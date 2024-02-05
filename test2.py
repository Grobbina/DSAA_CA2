import re

statement = "-3y"
var = "2x-20"
#Get all the variables on the right side of the equation
#find all "words" on the expression side of the equation (statement)
match = re.findall('([+-]?\d*[a-z])', statement)
#Move it to the left side of the equation
tomove = match
#Find all the numbers in the left side of the equation
match = re.findall(r'([+-]?\d+)\b(?!\w)', var)
#Move it to the right side of the equation
tomove2 = match
numbers = [int(num) for num in tomove2 if num]
# Calculate the sum
total_sum = sum(numbers)
#Remove the numbers from the left
var = re.sub(r'([+-]?\d+)\b(?!\w)', '', var)
statement = ''
if total_sum:
    if str(total_sum)[:1] == '-':
        statement = f'{str(total_sum)[1:]}'
    else:
        statement = f'-{total_sum}'
#move the variable to the left side of the equation
for i in tomove:
    if i[0] != '+' and i[0] != '-':
        var += f'-{i}'
    elif i[0] == '-':
        var += f'+{i[1:]}'
    else:
        var += f'-{i[1:]}'
print(var)
