import numpy as np


def bool_from_str(text: str) -> bool:
    if text.lower() == 'true':
        return True
    if text.lower() == 'false':
        return False


def empty_to_none(input_list):
    if not input_list:
        return None
    return input_list


def nan_to_zero(values):
    values[np.isnan(values)] = 0
    return values
