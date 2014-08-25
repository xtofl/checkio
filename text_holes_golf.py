import re
from itertools import starmap

def row_matches(lines, col):
    match = lambda line, r: re.match(r, line[col-1:col+2])
    spliced = starmap(match, zip(lines, [r"\S\S\S", r"\S\s\S", r"\S\S\S"]))
    return all(spliced)

def golf(text):
    n = 0
    for row in xrange(1, len(text)-1):
        lines = text[row-1:row+2]
        for col in xrange(1, len(lines[1])):
            if row_matches(lines, col):
                n += 1
    return n