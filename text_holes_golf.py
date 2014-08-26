import re
golf=lambda t:sum([len(filter(lambda c:re.match(r"\S\S\S\S\s\S\S\S\S", t[r-1][c-1:c+2]+t[r][c-1:c+2]+t[r+1][c-1:c+2]),xrange(1,len(t[r]))))for r in xrange(1,len(t)-1)])

def length(ts):
    return max(map(len, ts))

def eq(ts):
    return map(lambda line: line + " "*(length(ts) - len(line)), ts)

def golf(t):
    j = "".join(eq(t))
    m = length(t)
    match = lambda t: re.match(r"\S\S\S.{{{n}}}\S\s\S.{{{n}}}\S\S\S".format(n=m-3), t)
    return len(filter(match, [j[c:] for c in xrange(len(j))]))