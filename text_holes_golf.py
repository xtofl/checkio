import re
golf=lambda t:len(re.findall(r"(?=({s}.{{17}}\S\s\S.{{17}}{s}))".format(s="\S"*3),"".join(map(lambda l:l+" "*(20-len(l)),t))))