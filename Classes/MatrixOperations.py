import re
import numpy as np

class MatrixOperation:
    def __init__(self, input_string):
        self.input_string = input_string
        self.matrix_pattern = r"\[\[\s*(.*?)\s*\](?:,\s*\[\s*(.*?)\s*\])?\]"
        self.vector_pattern = r"\[\s*(.*?)\s*\]\s*([\+\-\*/]|(?:\*\*))\s*\[\s*(.*?)\s*\]"
        self.operator_pattern = r"(\+|\-|\*|\/|\*\*)"
        self.matrix_match = re.findall(self.matrix_pattern, self.input_string)
        self.vector_match = re.search(self.vector_pattern, self.input_string)
        self.operator_match = re.search(self.operator_pattern, self.input_string)

    def parse_matrices(self):
        try:
            if self.matrix_match:
                matrix1 = np.array([list(map(float, row.split(','))) for row in self.matrix_match[0]])
                matrix2 = np.array([list(map(float, row.split(','))) for row in self.matrix_match[1]])
                return matrix1, matrix2
            elif self.vector_match:
                vector1 = np.array(list(map(float, re.split(r'\s*,\s*', self.vector_match.group(1)))))
                vector2 = np.array(list(map(float, re.split(r'\s*,\s*', self.vector_match.group(3)))))
                # Transpose vectors if they are column vectors
                return vector1, vector2
            else:
                raise ValueError("Invalid input. Unable to determine matrix or vector format.")
        except ValueError:
            raise ValueError("Invalid matrix or vector format. Ensure all elements are valid numbers.")

    def validate_shapes(self, operand1, operand2):
        if isinstance(operand1, np.ndarray) and isinstance(operand2, np.ndarray):
            if self.operator_match.group() == '*' and operand1.shape[0] != operand2.shape[0]:
                raise ValueError("Incompatible matrix shapes for multiplication.")
        elif isinstance(operand1, np.ndarray) and isinstance(operand2, np.ndarray):
            if self.operator_match.group() == '*' and len(operand1) != len(operand2):
                raise ValueError("Incompatible vector sizes for element-wise multiplication.")

    def perform_operation(self):
        try:
            if self.matrix_match or self.vector_match:
                operand1, operand2 = self.parse_matrices()
                self.validate_shapes(operand1, operand2)
                operator = self.operator_match.group()

                if self.matrix_match:
                    if operator == '+':
                        result = operand1 + operand2
                    elif operator == '-':
                        result = operand1 - operand2
                    elif operator == '*':
                        result = np.dot(operand1, operand2)
                    elif operator == '/':
                        result = operand1 / operand2
                    elif operator == '**':
                        result = np.linalg.matrix_power(operand1, int(operand2))
                elif self.vector_match:
                    if operator == '+':
                        result = operand1 + operand2
                    elif operator == '-':
                        result = operand1 - operand2
                    elif operator == '*':
                        result = operand1 * operand2
                    elif operator == '/':
                        result = operand1 / operand2
                    elif operator == '**':
                        result = operand1 ** operand2

                return np.round(result, decimals=2)  # Round for better readability
            else:
                return None
        except ValueError as ve:
            return f"Error: {str(ve)}"




# Example usage:
input_string_matrix = "[[1,2],[3,4]]*[[5,6],[7,8]]"
matrix_operation_matrix = MatrixOperation(input_string_matrix)
result_matrix = matrix_operation_matrix.perform_operation()
print(result_matrix)

input_string_vector = "[1,2,3]*[4,5,6]"
matrix_operation_vector = MatrixOperation(input_string_vector)
result_vector = matrix_operation_vector.perform_operation()
print(result_vector)
