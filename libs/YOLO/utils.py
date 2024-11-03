import pickle
import pathlib
import ultralytics
import numpy as np

from pydantic import BaseModel, PositiveFloat, PositiveInt, ConfigDict
from typing import List


def save_object(obj, path):
    with open(path, 'wb') as file:
        pickle.dump(obj, file)

def load_object(path):
    with open(path, 'rb') as file:
        return pickle.load(file)
    
def parse_yolo_box(box):
    return {'all_ap': box.all_ap,
            'ap': box.ap,
            'ap50': box.ap50,
            'ap_class_index': box.ap_class_index,
            'curves': box.curves,
            'curve_results': box.curves_results,
            'f1': box.f1,
            'f1_curve': box.f1_curve,
            'map': box.map,
            'map50': box.map50,
            'map75': box.map75,
            'maps': box.maps,
            'mp': box.mp,
            'mr': box.mr,
            'nc': box.nc,
            'p': box.p,
            'p_curve': box.p_curve,
            'prec_values': box.prec_values,
            'px': box.px,
            'r': box.r,
            'r_curve': box.r_curve}

def parse_yolo_results(results):
    return {'ap_class_index': results.ap_class_index,
            'box': parse_yolo_box(results.box),
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

class ParseYOLOBox(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed = True)
    all_ap: np.ndarray
    ap: np.ndarray
    ap50: np.ndarray
    ap_class_index: np.ndarray
    curves: List
    curve_results: List
    f1: np.ndarray
    f1_curve: np.ndarray
    map: PositiveFloat
    map50: PositiveFloat
    map75: PositiveFloat
    maps: np.ndarray
    mp: PositiveFloat
    mr: PositiveFloat
    nc: PositiveInt
    p: np.ndarray
    p_curve: np.ndarray
    prec_values: np.ndarray
    px: np.ndarray
    r: np.ndarray
    r_curve: np.ndarray


class ParseYOLOResults(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed = True)
    ap_class_index: np.ndarray
    box: ParseYOLOBox
    confusion_matrix: ultralytics.utils.metrics.ConfusionMatrix
    curves: List[str]
    curves_results: List
    plot: bool
    results_dict: dict[str, PositiveFloat]
    fitness: float
    keys: List[str]
    maps: np.ndarray
    names: dict[int, str]
    save_dir: pathlib.Path
    speed: dict[str, PositiveFloat]
    task: str

class YOLOResults(BaseModel):
    train: ParseYOLOResults
    val: ParseYOLOResults
    test: ParseYOLOResults