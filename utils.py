from math import log10

letter_values = {"": 1,
                 "K": 1000,
                 "M": 1000000,
                 "B": 1000000000}

ends = list(letter_values.keys())

def human_number(num):
    '''
    Takes an int/float e.g. 10000 and returns a formatted version e.g. 10k
    '''

    if isinstance(num, str):
        return num
    
    if num < 1: return 0

    rounded = round(num, 3 - int(log10(num)) - 1)
    suffix = ends[int(log10(rounded)/3)]
    new_num = str(rounded / letter_values[suffix])
    if new_num.endswith(".0"):
        new_num = new_num[:-2]
    return str(new_num)+suffix


