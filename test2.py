import re 

statement = '50-3x+50-60'
#extract only numerics not followed by a letter but following a + or - sign
matchno = re.findall(r'(?<=[+-])\d+(?![a-zA-Z])', statement)
print(matchno)
