import numpy as np


def bool_from_str(text: str) -> bool:
    if text.lower() == 'true':
        return True
    if text.lower() == 'false':
        return False


def empty_to_none(input_list_or_dict):
    if not input_list_or_dict:
        return None
    return input_list_or_dict


def nan_to_zero(values):
    values[np.isnan(values)] = 0
    return values


def ichimoku_cloud(in_real):
    if not in_real:
        return [], [], [], [], []
    length = len(in_real)
    tenkan = [0] * min(9, length)
    kijun = [0] * min(26, length)
    senkou_a = [0] * min(26, length)
    senkou_b = [0] * min(52, length)
    chikou = [0] * min(26, length)
    for i in range(length):
        if i >= 9:
            min_val, max_val = min_max(in_real[i - 9:i])
            tenkan.append((min_val + max_val) / 2)
        if i >= 26:
            min_val, max_val = min_max(in_real[i - 26:i])
            kijun.append((min_val + max_val) / 2)
            senkou_a.append((tenkan[i] + kijun[i]) / 2)
            chikou.append(in_real[i - 26])
        if i >= 52:
            min_val, max_val = min_max(in_real[i - 52:i])
            senkou_b.append((min_val + max_val) / 2)

    senkou_a = ([0] * 26) + senkou_a[:-26]
    senkou_b = ([0] * 26) + senkou_b[:-26]
    return tenkan, kijun, senkou_a, senkou_b, chikou


def min_max(in_real):
    min_val = in_real[0]
    max_val = in_real[0]
    for price in in_real:
        if min_val > price:
            min_val = price
        if max_val < price:
            max_val = price
    return min_val, max_val
