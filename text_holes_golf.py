import re

def golf(t):
    m = max(map(len, t))
    j = "".join(map(lambda l: l + " "*(m - len(l)), t))
    return len(filter(lambda t: re.match(r"\S\S\S.{{{n}}}\S\s\S.{{{n}}}\S\S\S".format(n=m-3), t), [j[c:] for c in xrange(len(j))]))