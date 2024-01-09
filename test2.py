import re

var = 'a'
var_coeff = re.search(r'([+-]?\d*)[a-zA-Z]', var)

print(var_coeff.group(1))