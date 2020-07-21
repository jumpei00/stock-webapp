import numpy as np


def empty_to_none(input_list):
    if not input_list:
        return None
    return input_list


def nan_to_zero(values):
    values[np.isnan(values)] = 0
    return values
