from __future__ import division
import math
from web.constants import RAINBOW

def getRainbowFromSize(size):
    if not size:
        return []
    if size > len(RAINBOW):
        return (RAINBOW * int(math.ceil(size / len(RAINBOW))))[:size]
    step = int(round(len(RAINBOW) / size))
    new_rainbow = []
    i = 0
    while i < len(RAINBOW):
        new_rainbow.append(RAINBOW[i])
        i += step
    if len(new_rainbow) < size:
        new_rainbow.append(RAINBOW[-1])
    return new_rainbow
