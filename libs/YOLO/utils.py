import pickle

def save_object(obj, path):
    with open(path, 'wb') as file:
        pickle.dump(obj, file)

def load_object(path):
    with open(path, 'rb') as file:
        return pickle.load(file)
    
def parse_yolo_results(results):
    return {'ap_class_index': results.ap_class_index,
            'box': results.box,
            'confusion_matrix': results.confusion_matrix,
            'curves': results.curves,
            'curves_results': results.curves_results,
            'plot': results.plot,
            'results_dict': results.results_dict,
            'fitness': results.fitness,
            'keys': results.keys,
            'maps': results.maps,
            'names': results.names,
            'save_dir': results.save_dir,
            'speed': results.speed,
            'task': results.task}