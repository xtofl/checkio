import re
golf = lambda t: sum([len(filter(lambda c: re.match(r"\S\S\S\S\s\S\S\S\S", t[r-1][c-1:c+2] + t[r][c-1:c+2] + t[r+1][c-1:c+2]), xrange(1, len(t[r])))) for r in xrange(1, len(t)-1)])