import re
from itertools import starmap

r1 = r"\S\S\S\S\s\S\S\S\S"

def golf(t):
    n = 0

    for r in xrange(1, len(t)-1):
        n += len(filter(lambda c: re.match(r1, t[r-1][c-1:c+2] + t[r][c-1:c+2] + t[r+1][c-1:c+2]),
                        xrange(1, len(t[r]))))
    return n