import re

def row_matches(lines, col):
    return all(map(lambda r: len(r) > col+2, lines)) and \
           all([
                re.match(r"\S\S\S", lines[0][col-1:]),
                re.match(r"\S\s\S", lines[1][col-1:]),
                re.match(r"\S\S\S", lines[2][col-1:])])

def golf(text):
    def iterate(text):
        for row in xrange(1, len(text)-1):
            lines = text[row-1:row+2]
            for col in xrange(1, len(lines[row])):
                if row_matches(lines, col): yield row, col
    return len(list(iterate(text)))