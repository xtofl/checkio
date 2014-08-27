import re

def golf(t):
    m = max(map(len, t))
    return len(re.findall(r"(?=(\S\S\S.{{{n}}}\S\s\S.{{{n}}}\S\S\S))".format(n=m-3), "".join(map(lambda l: l + " "*(m - len(l)), t))))