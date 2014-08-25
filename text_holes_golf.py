import re

def row_matches(lines, col):
    if all(map(lambda r: len(r) > col+1, lines)):
        splice = lambda line: line[col-1:col+2]
        spliced = map(splice, lines)
        return all([
            re.match(r"\S\S\S", spliced[0]),
            re.match(r"\S\s\S", spliced[1]),
            re.match(r"\S\S\S", spliced[2])])

def golf(text):
    def iterate(text):
        for row in xrange(1, len(text)-1):
            lines = text[row-1:row+2]
            for col in xrange(1, len(lines[row])):
                if row_matches(lines, col):
                    print row, col
                    yield row, col
    return len(list(iterate(text)))