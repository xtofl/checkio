import re
from itertools import starmap

def golf(text):
    n = 0
    for row in xrange(1, len(text)-1):
        lines = text[row-1:row+2]
        for col in xrange(1, len(lines[1])):
            r1 = r"\S"*3
            r2 = r"\S\s\S"
            n += all(starmap(lambda line, r: re.match(r, line[col-1:col+2]),
                        zip(lines, [r1, r2, r1])))
    return n