import re

expr = -16.02

 

print(re.sub(r".0+$", "", str(expr)))