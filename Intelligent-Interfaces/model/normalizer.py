import numpy as np


def normalize_values(values_from: np.ndarray, scale_min = 0.0, scale_max = 1.0):
    current_max = np.max(values_from)
    current_min = np.min(values_from)
    a = (scale_max - scale_min) / (current_max - current_min)
    b = scale_min - a * current_min
    return a * values_from + b
