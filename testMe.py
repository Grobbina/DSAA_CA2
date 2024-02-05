import re
import numpy as np

expression = "[[1,2],[3,4]]+[[5,6],[7,8]]"
matrix_pattern = r"\[\[(.*?)\],\s*\[\s*(.*?)\]\]"

matches = re.findall(matrix_pattern, expression)
print('matches', matches)


# Perform matrix addition

# Convert strings to numerical matrices using map and int
matrix1 = np.array([list(map(int, row.split(','))) for row in matches[0]])
matrix2 = np.array([list(map(int, row.split(','))) for row in matches[1]])
print('matrix1Final', matrix1)
print('matrix2Final', matrix2)
result_matrix =matrix1 +matrix2
print('finalresult',result_matrix)



import re
import numpy as np

def parse_matrix_expression(expression):
    # Define regular expressions for matrix and operator extraction
    matrix_pattern = r"\[\[([0-9,]+)\],\[([0-9,]+)\]\]"
    operator_pattern = r"(\+|\-|\*|\/|\*\*)"

    # Extract matrices and operator
    matrices = re.findall(matrix_pattern, expression)
    operator = re.findall(operator_pattern, expression)

    # Convert strings to numpy arrays
    matrix1 = np.array([list(map(int, mat[0].split(','))) for mat in matrices[:1]])
    matrix2 = np.array([list(map(int, mat[1].split(','))) for mat in matrices[1:]])

    return matrix1, matrix2, operator[0]

def evaluate_matrix_expression(matrix1, matrix2, operator):
    if operator == '+':
        result = matrix1 + matrix2
    elif operator == '-':
        result = matrix1 - matrix2
    elif operator == '*':
        result = matrix1 * matrix2
    elif operator == '/':
        try:
            result = matrix1 / matrix2
        except ZeroDivisionError:
            raise ValueError("Division by zero is not allowed")
    elif operator == '**':
        result = matrix1 ** matrix2
    else:
        raise ValueError("Unsupported operator")

    return result

# Example usage
expression = "[[1,2],[3,4]]*[[5,6],[7,8]]"
matrix1, matrix2, operator = parse_matrix_expression(expression)
result = evaluate_matrix_expression(matrix1, matrix2, operator)

print("Matrix 1:")
print(matrix1)
print("Matrix 2:")
print(matrix2)
print("Operator:", operator)
print("Result:")
print(result)
