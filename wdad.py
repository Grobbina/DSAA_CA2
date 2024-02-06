import re

# Define the regex pattern to check for operators
pattern = r'[+\-*/]'

# Test string
test_string = "3 + 4 - 5 * 6 / 2"

# Find all occurrences of operators in the test string
operators = re.findall(pattern, test_string)

print("Operators found:", operators)
