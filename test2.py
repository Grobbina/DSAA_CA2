import re

equation = '3x+y+4y+2x'

terms = re.findall(r'([-+]?\s*\d*\s*[a-zA-Z])', equation)

print(''.join(terms))
