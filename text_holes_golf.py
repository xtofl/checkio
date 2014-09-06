import re
golf=lambda t:len(re.findall(r"(?=(\S\S\S.{27}\S\s\S.{27}\S\S\S))","".join([l.ljust(30," ") for l in t])))