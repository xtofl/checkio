import re

def matches(line):
    return re.finditer(r"\S\s\S", line)

def golf(text):
    def iterate(text):
        for i, line in enumerate(text[1:-1]):
            for s in matches(line):
                isalpha = lambda n: re.match(r"\S{3}", text[n][s.start():s.end()])
                neighbors = map(isalpha, [i, i+2])
                if all(neighbors):
                    yield i, s
    return len(list(iterate(text)))