import re
import turtle
import numpy as np
from Classes.BinaryTree import BinaryTree
from Classes.Stack import Stack

class MatrixOperations(BinaryTree):
    def __init__(self, expression, storage=None):
        super().__init__('?')
        self.expression = expression
        #self.tokens = re.findall(r'\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|\*\*|[+\-*/()]|\[|\]', expression)
        self.tokens = re.findall(r'\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|\*\*|[+\-*/()]|\[|\]', expression)

        self.current_index = 0
        self.storage = storage or {}
        self.tree = self.build()

    def build(self):
        stack = Stack()
        tree = BinaryTree('?')
        stack.push(tree)
        currentTree = tree

        for t in self.tokens:
            if t == '[':
                currentTree.insertLeft('?')
                stack.push(currentTree)
                currentTree = currentTree.getLeftTree()

            elif t == ']':
                currentTree = stack.pop()

            elif t in ['+', '-', '*', '/', '**']:
                while (not stack.isEmpty() and
                    stack.peek().getKey() in ['+', '-', '*', '/', '**'] and
                    self._get_precedence(t) <= self._get_precedence(stack.peek().getKey())):
                    currentTree = stack.pop()

                currentTree.setKey(t)
                currentTree.insertRight('?')
                stack.push(currentTree)
                currentTree = currentTree.getRightTree()

            elif t not in ['+', '-', '*', '/', ')', '**', '[', ']']:
                if '[' in t:
                    currentTree.setKey(self._parse_matrix(t))
                elif t.isalpha():
                    currentTree.setKey(t)
                else:
                    currentTree.setKey(float(t))
                parent = stack.pop()
                currentTree = parent

        return tree

    def _get_precedence(self, operator):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '**': 3}
        return precedence.get(operator, 0)


    def _parse_matrix(self, matrix_str):
        matrix_str = matrix_str[1:-1]  # Remove brackets
        rows = matrix_str.split(';')
        matrix = []
        for row in rows:
            elements = [float(e) for e in row.split(',')]
            matrix.append(elements)
        return np.array(matrix)

    def evaluate(self):
        return self._evaluate_recursive(self.tree)

    def _evaluate_recursive(self, tree):
        if tree is None:
            return None

        if isinstance(tree.getKey(), np.ndarray):
            return tree.getKey()

        operator = tree.getKey()
        left_value = self._evaluate_recursive(tree.getLeftTree())
        right_value = self._evaluate_recursive(tree.getRightTree())

        if left_value is None or right_value is None:
            return None

        if operator == '+' or operator == '-' or operator == '*' or operator == '/':
            if isinstance(left_value, np.ndarray) and isinstance(right_value, np.ndarray):
                return self._matrix_operation(operator, left_value, right_value)
            else:
                raise ValueError("Invalid matrix operation or operands")

        if operator == '**':
            if isinstance(left_value, np.ndarray) and isinstance(right_value, (int, float)):
                return left_value ** right_value
            else:
                raise ValueError("Invalid matrix operation or operands")

        return self._get_variable_value(operator, left_value, right_value)


    def _matrix_operation(self, operator, matrix1, matrix2):
        if operator == '+':
            return np.add(matrix1, matrix2)
        elif operator == '-':
            return np.subtract(matrix1, matrix2)
        elif operator == '*':
            return np.dot(matrix1, matrix2)
        else:
            return None

    def _get_variable_value(self, variable, left_value, right_value):
        return self.storage.get(variable, None) or right_value

    def printInorder(self, level):
        leftTree = self.tree.getLeftTree()
        rightTree = self.tree.getRightTree()
        if rightTree is not None:
            rightTree.printInorder(level + 1)
        print(str(level * '-') + str(self.tree.getKey()))
        if leftTree is not None:
            leftTree.printInorder(level + 1)

    def is_digit_neg(self, n: str) -> bool:
        try:
            int(n)
            return True
        except ValueError:
            return False

    def __str__(self):
        return self.expression


if __name__ == '__main__':
    matrix_tree = MatrixOperations('[[1,2],[3,4]]+[[5,6],[7,8]]')
    matrix_tree.printInorder(0)
    print(matrix_tree.evaluate())
    print(matrix_tree)
