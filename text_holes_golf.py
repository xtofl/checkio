import re
from itertools import starmap

def golf(t):
    n = 0
    for row in xrange(1, len(t)-1):
        ls = t[row-1:row+2]
        for c in xrange(1, len(ls[1])):
            r = r"\S"*3
            s = r"\S\s\S"
            n += all(starmap(lambda l, r: re.match(r, l[c-1:c+2]),
                        zip(ls, [r, s, r])))
    return n