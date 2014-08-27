import re
def golf(t):
    m=max(map(len, t))
    return len(re.findall(r"(?=({s}.{{{n}}}\S\s\S.{{{n}}}{s}))".format(n=m-3,s="\S\S\S"),"".join(map(lambda l:l+" "*(m-len(l)),t))))