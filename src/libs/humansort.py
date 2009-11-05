# -*- coding: iso-8859-15 -*-

import re
from itertools import groupby

# The code extended with suitable renamings:
spec_dict = {'Å':'A', 'Ä':'A'}

def spec_order(s):
    return ''.join([spec_dict.get(ch, ch) for ch in s])
    
def trynum(s):
    try:
        return float(s)
    except:
        return spec_order(s)

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ trynum(c) for c in re.split('([0-9]+\.?[0-9]*)', s) ]

def humansort(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

