# import libraries
from libs.__init__ import *

import os
import shutil
import re
import pandas as pd
import numpy as np

from collections import Counter

# declare functions to clean files

# create a function that get messy words
def get_nasty_files(files_to_remove, list_of_words):
  nasty_files = list()
  for filter_word in files_to_remove:
    nasty_files.extend([word for word in list_of_words if filter_word.upper() in word.upper()])
  return nasty_files

# create a function to delete files
def delete_nasty_files(path, files_to_remove):
  # get files list
  list_files = os.listdir(path)

  # gest nasty files
  nasty_files = get_nasty_files(files_to_remove, list_files)

  # validate if exists then remove it
  if len(nasty_files) > 0:
    for file in nasty_files:
      file_path = f'{path}/{file}'
      # check if exists
      if os.path.exists(file_path):
          os.remove(file_path)

# function to get group name
def get_group_name(group_label, zfill = 6):
      # get upper and lower bounds
    lower_bound = group_label.split('-')[0]
    upper_bound = group_label.split('-')[1]

    # obtain group name
    group_name = f"Grupo_{lower_bound.zfill(zfill)}_{upper_bound.zfill(zfill)}"

    return lower_bound, upper_bound, group_name

# function to remove nasty files on each group
def clean_nasty_files_from_group(input_path, group_label, files_to_remove):
    # obtain group name
    _, _, group_name = get_group_name(group_label)

    # get path
    group_path = f'{input_path}/{group_name}'

    # clean first nasty files
    delete_nasty_files(group_path, files_to_remove)

    # get labels' path
    label_path = f'{group_path}/labels'

    # clean second nasty files
    delete_nasty_files(label_path, files_to_remove)

# function to copy all txt files from a folder to another one
def copy_txt_files(input_path, group_label, destination_folder):
  # get group name
  _, _, group_name = get_group_name(group_label)

  # get group path
  source_folder = f'{input_path}/{group_name}/labels'

  # ensure the source folder exists
  if not os.path.exists(source_folder):
      raise ValueError(f"Source folder does not exist: {source_folder}")

  # create the destination folder if it doesn't exist
  os.makedirs(destination_folder, exist_ok = True)

  # list all files in the source folder
  for filename in os.listdir(source_folder):
    if filename.endswith('.txt'):
        # construct full file path
        src_file = os.path.join(source_folder, filename)
        dest_file = os.path.join(destination_folder, filename)

        # copy the file
        shutil.copy2(src_file, dest_file)

def copy_img_files(group_label, source_folder, destination_folder):
  # Ensure the source folder exists
  if not os.path.exists(source_folder):
    raise ValueError(f"Source folder does not exist: {source_folder}")
  
  # create the destination folder if it doesn't exist
  os.makedirs(destination_folder, exist_ok = True)

  # get upper and lower bounds
  lower_bound, upper_bound, _ = get_group_name(group_label)

  # convert into integers
  lower_bound = int(lower_bound)
  upper_bound = int(upper_bound)

  # only images that are between lower and upper bound
  img_files = [img for img in os.listdir(source_folder) if '.png' in img.lower()]
  img_files_sel = [img for img in img_files if int(img.split('_')[-1].split('.')[0]) >= lower_bound and 
                                               int(img.split('_')[-1].split('.')[0]) <= upper_bound]

  # copy files
  if len(img_files_sel) > 0:
    for filename in img_files_sel:
      # construct full file path
      src_file = os.path.join(source_folder, filename)
      dest_file = os.path.join(destination_folder, filename)
     
      # copy the file
      shutil.copy2(src_file, dest_file)

def retrieve_labels_from_group(group_path):
    # get txts
    path = os.path.join(group_path, 'labels')
    txts = sorted(os.listdir(path))

    # Create pattern to identify the image number
    pattern = '[0-9]+'

    # Declare a dictionary for equivalence
    label_equivalence = {'image': 'image',
                         0: 'D00',
                         1: 'D10',
                         2: 'D20',
                         3: 'D40'}
    
    # Declare empty list to store each register
    records = list()

    # iterate over txt files
    for txt in txts:
        # get image number
        img_num = int(re.findall(pattern, txt)[0])

        # grab path
        txt_path = os.path.join(path, txt)

        # read txt file
        with open(txt_path, 'r') as file:
            content = file.read()

        # get labels per image
        labels = [int(line[0]) for line in content.split('\n') if line != '']

        # get unique values
        unique = dict(Counter(labels))
        unique_sel = unique.copy()

        # add remaining labels
        for lbl in [0, 1, 2, 3]:
            if lbl not in unique:
                unique_sel[lbl] = 0

        # sort dict
        unique_sel = dict(sorted(unique_sel.items()))

        # create record
        record = dict()
        record['image'] = img_num
        record.update(unique_sel)

        # save record
        records.append(record)

    # convert into dataframe
    records = pd.DataFrame(records)
    records.columns = records.columns.map(label_equivalence)

    return records

def retrieve_labels_from_rdd2022(label_root_path, subset):
    # get txts
    path = os.path.join(label_root_path, subset)
    txts = sorted(os.listdir(path))

    # Create pattern to identify the image number
    pattern = '[0-9]+'

    # Declare a dictionary for equivalence
    label_equivalence = {'image': 'image',
                         0: 'D00',
                         1: 'D10',
                         2: 'D20',
                         3: 'D40'}
    
    # Declare empty list to store each register
    records = list()

    # iterate over txt files
    for txt in txts:
        # get image number
        img_num = int(re.findall(pattern, txt)[0])

        # grab path
        txt_path = os.path.join(path, txt)

        # read txt file
        with open(txt_path, 'r') as file:
            content = file.read()

        # get labels per image
        labels = [int(line[0]) for line in content.split('\n') if line != '']

        # get unique values
        unique = dict(Counter(labels))
        unique_sel = unique.copy()

        # add remaining labels
        for lbl in [0, 1, 2, 3]:
            if lbl not in unique:
                unique_sel[lbl] = 0

        # sort dict
        unique_sel = dict(sorted(unique_sel.items()))

        # create record
        record = dict()
        record['image'] = img_num
        record.update(unique_sel)

        # save record
        records.append(record)

    # convert into dataframe
    records = pd.DataFrame(records)
    records.columns = records.columns.map(label_equivalence)

    return records

def clean_folder(folder_path):
  shutil.rmtree(folder_path)
  os.makedirs(folder_path)

def distribute_images(images_df, img_in_path, lbl_in_path, img_out_path_root, lbl_out_path_root, subsets = ['train', 'val', 'test']):
    for subset in subsets:
        # get image index
        img_idx = images_df.loc[images_df['subset'] == subset, 'image'].tolist()

        # get paths
        img_path = os.path.join(img_out_path_root, subset)
        lbl_path = os.path.join(lbl_out_path_root, subset)

        # clean folfers
        clean_folder(img_path)
        clean_folder(lbl_path)

        # get images and labels
        imgs = [img_name for img_name in sorted(os.listdir(img_in_path)) 
                if int(re.findall('[0-9]+', img_name)[0]) in img_idx]
        
        lbls =  [img_name for img_name in sorted(os.listdir(lbl_in_path)) 
            if int(re.findall('[0-9]+', img_name)[0]) in img_idx]
        
        # copy the file
        for img, lbl in zip(imgs, lbls):
            img_path_source = os.path.join(img_in_path, img)
            lbl_path_source = os.path.join(lbl_in_path, lbl)

            shutil.copy2(img_path_source, img_path)
            shutil.copy2(lbl_path_source, lbl_path)

def save_experiment_labels(input_path, output_path, subsets = ['train', 'val', 'test']):
    # create output path
    for subset in subsets:
        # create subset path
        subset_output_path = f'{output_path}/{subset}'
        os.makedirs(subset_output_path, exist_ok = True)

        # read from input path
        subset_input_path = f'{input_path}/{subset}'

        # copy labels
        for label in os.listdir(subset_input_path):
            label_path_in = f'{subset_input_path}/{label}'
            label_path_out = f'{subset_output_path}/{label}'
            shutil.copy2(label_path_in, label_path_out)

def distribute_images_from_labels(img_in_path, lbl_in_path, img_out_path_root, lbl_out_path_root, subsets = ['train', 'val', 'test'], img_extension = 'png'):
    for subset in subsets:
        # get subset label path
        subset_label_in_path = f'{lbl_in_path}/{subset}'

        # get labels
        lbls = sorted(os.listdir(subset_label_in_path))

        # change their name to images
        imgs = [lbl.replace('txt', img_extension) for lbl in lbls]

        # get paths
        img_path = os.path.join(img_out_path_root, subset)
        lbl_path = os.path.join(lbl_out_path_root, subset)

        # clean folfers
        clean_folder(img_path)
        clean_folder(lbl_path)

        # copy the file
        for img, lbl in zip(imgs, lbls):
            img_path_source = os.path.join(img_in_path, img)
            lbl_path_source = os.path.join(subset_label_in_path, lbl)

            shutil.copy2(img_path_source, img_path)
            shutil.copy2(lbl_path_source, lbl_path)