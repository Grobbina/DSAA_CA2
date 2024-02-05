import re
import numpy as np

class MatrixOperation:
    def __init__(self, input_string):
        self.input_string = input_string
        self.matrix_pattern = r"\[\[(.*?)\],\s*\[\s*(.*?)\]\]"
        self.operator_pattern = r"(\+|\-|\*|\/|\*\*)"
        self.matrix_match = re.findall(self.matrix_pattern, self.input_string)
        self.operator_match = re.search(self.operator_pattern, self.input_string)

    def perform_operation(self):
        if self.matrix_match and self.operator_match:
            matrix1 = np.array([list(map(int, row.split(','))) for row in self.matrix_match[0]])
            matrix2 = np.array([list(map(int, row.split(','))) for row in self.matrix_match[1]])
            operator = self.operator_match.group()

            if operator == '+':
                result = matrix1 + matrix2
            elif operator == '-':
                result = matrix1 - matrix2
            elif operator == '*':
                result = np.dot(matrix1, matrix2)
            elif operator == '/':
                result = matrix1 / matrix2
            elif operator == '**':
                # Perform element-wise exponentiation
                result = np.power(matrix1, matrix2)

            return result
        else:
            return None

# Example usage
input_string = input('Enter a matrix:')
input_string= str(input_string)
matrix_operation = MatrixOperation(input_string)
result = matrix_operation.perform_operation()

if result is not None:
    print(result)
else:
    print("Invalid input format.")
