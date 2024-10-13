# import libraries
from libs.__init__ import *

# declare functions to clean files

def get_nasty_files(list_of_words):
  for filter_word in GLOB_FILES_TO_REMOVE:
    list_of_words = [word for word in list_of_words if filter_word.upper() in word.upper()]
  return list_of_words

# clean files from datasets
def clean_files(main_path):
    # get path
    for country, paths in main_path.items():
        print(f'Country: {country}')
        for path in paths:
            # get files
            files = get_nasty_files(os.listdir(path))
            # check if it has files to be removed:
            if len(files) > 0:
                for file in files:
                    file_path = f'{path}/{file}'
                    # check if exists
                    if os.path.exists(file_path):
                        os.remove(file_path)

# create a function to delete files
def delete_nasty_files(path):
  # get files list
  list_files = os.listdir(path)

  # gest nasty files
  nasty_files = get_nasty_files(list_files)

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
def clean_nasty_files_from_group(root_path, group_label):
    # obtain group name
    _, _, group_name = get_group_name(group_label)

    # get path
    group_path = f'{root_path}/{group_name}'

    # clean first nasty files
    delete_nasty_files(group_path)

    # get labels' path
    label_path = f'{group_path}/labels'

    # clean second nasty files
    delete_nasty_files(label_path)

# function to copy all txt files from a folder to another one
def copy_txt_files(root_path, group_label, destination_folder):
  # get group name
  _, _, group_name = get_group_name(group_label)

  # get group path
  source_folder = f'{root_path}/{group_name}/labels'

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