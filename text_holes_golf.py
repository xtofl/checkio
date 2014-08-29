import re
golf=lambda t:len(re.findall(r"(?=(\S\S\S.{27}\S\s\S.{27}\S\S\S))","".join(map(lambda l:l.ljust(30, " "),t))))