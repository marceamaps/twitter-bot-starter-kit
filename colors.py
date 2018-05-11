from itertools import chain
import matplotlib
from errors import UnknownColorError

def double_short_hex(shx):
    return '#' + ''.join(chain(*zip(shx[1:], shx[1:])))

def read_color(color_string):
    if color_string.rule_name != 'color_string':
        raise ValueError('Expected this function to be called with a color_string. received ' + color_string.rule_name)
    if color_string[0].rule_name == 'hex_color':
        hex_string = color_string[0].value
        if len(hex_string) < 7:
            return double_short_hex(hex_string)
        return hex_string
    elif color_string[0].rule_name == 'lowercase_word':
        try:
            return matplotlib.colors.cnames[color_string[0].value]
        except KeyError as e:
            raise UnknownColorError(e)
    elif color_string[0].rule_name == 'color_string':
        # I don't know why this happens, but w/e
        return read_color(color_string[0])
    else:
        raise ValueError('Unknown format for color string ' + color_string[0].rule_name)
