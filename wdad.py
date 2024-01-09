# import re

# # Example string: "3x + 2y - 5z"
# equation_str = "50+3x+2y-5z+8"

# # Define a regular expression pattern to match the coefficient of a variable
# pattern = re.compile(r'([+-]?\d*)[a-zA-Z]')

# # Find all matches in the string
# matches = pattern.findall(equation_str)

# # Remove the variables and their coefficients from the string
# for match in matches:
#     equation_str = equation_str.replace(match, '')

# # remove the variable itself from the string
# equation_str = re.sub(r'[a-zA-Z]', '', equation_str)

# print(equation_str)



import re

# Example string: "3x + 2y - 5z"
equation_str = "3x+5x"

# Define a regular expression pattern to match the coefficient of a variable
pattern = re.compile(r'([+-]?\d*)[a-zA-Z]')

# Find all matches in the string
matches = pattern.findall(equation_str)

# Remove the variables and their coefficients from the string
for match in matches:
    equation_str = equation_str.replace(match, '')

print(equation_str)
