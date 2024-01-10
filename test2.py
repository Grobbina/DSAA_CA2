import re 
from Classes.ParseTree import ParseTree

statement = '41'
#extract only numerics not followed by a letter as well as the operator before
matchno = re.findall(r'(\+?-?\d+(?![a-zA-Z]))', statement)
print(matchno)
evaluated = sum([int(i) for i in matchno])
for match in matchno:
    statement = statement.replace(match, '')
statement = f'{evaluated}+{statement}'
tree = ParseTree(statement)
print(statement)
