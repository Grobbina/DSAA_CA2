import re
from Classes.BinaryTree import BinaryTree
from Classes.Stack import Stack
import numpy as np

class MatrixTree(BinaryTree):
    def __init__(self, expression, storage=None):
        super().__init__('?')
        self.expression = expression
        # Updated regex to handle matrix expressions
        self.tokens = re.findall(r'\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|\*\*|[+\-*/()]|\[\[.+?\]\]', expression)

        # Check for negatives and insert missing multiplication operators
        loop = len(self.tokens) - 1
        i = 0
        while loop > 0:
            if self.tokens[i] in ['*', '/', '(',')'] and self.tokens[i + 1] == '-':
                # Check that the next token is a number
                if self.is_digit_neg(self.tokens[i + 2]):
                    del self.tokens[i + 1]
                    loop -= 1
                    self.tokens[i + 1] = f'-{self.tokens[i + 1]}'
                else:
                    self.tokens[i + 1] = f'-1'
                    self.tokens.insert(i + 2, '*')
                    loop += 1
            loop -= 1
            i += 1

            if self.tokens[i] == '-' and self.tokens[i + 1] == '-':
                del self.tokens[i]
                self.tokens[i] = '+'
                loop -= 1
            if self.tokens[i] == '+' and self.tokens[i + 1] == '-':
                del self.tokens[i]
                loop -= 1
        # If tokens are a number followed by a variable, add a * between them
        for i in range(len(self.tokens) - 1):
            if self.is_digit_neg(self.tokens[i]) and self.tokens[i + 1].isalpha():
                self.tokens.insert(i + 1, '*')
                # Insert brackets as well
                self.tokens.insert(i, '(')
                self.tokens.insert(i + 4, ')')
        # If a number is followed by an opening bracket, add a * between them
        for i in range(len(self.tokens) - 1):
            if self.is_digit_neg(self.tokens[i]) and self.tokens[i + 1] == '(':
                self.tokens.insert(i + 1, '*')
        self.current_index = 0
        self.storage = storage or {}
        self.tree = self.build()

    def build(self):
        stack = Stack()
        tree = BinaryTree('?')
        stack.push(tree)
        currentTree = tree

        for t in self.tokens:
            if t == '(':
                currentTree.insertLeft('?')
                stack.push(currentTree)
                currentTree = currentTree.getLeftTree()

            elif t in ['+', '-', '*', '/', '**']:
                currentTree.setKey(t)
                currentTree.insertRight('?')
                stack.push(currentTree)
                currentTree = currentTree.getRightTree()

            elif t == ')':
                currentTree = stack.pop()

            elif t not in ['+', '-', '*', '/', ')', '**']:
                if t.isalpha():
                    currentTree.setKey(t)
                else:
                    currentTree.setKey(float(t))
                parent = stack.pop()
                currentTree = parent

        return tree

    def evaluate(self):
        return self._evaluate_recursive(self.tree)

    def _evaluate_recursive(self, tree):
        if tree is None:
            return None

        if isinstance(tree.getKey(), float):
            return tree.getKey()
        elif isinstance(tree.getKey(), list):  # Handle matrix operations
            return self._evaluate_matrix(tree)

        operator = tree.getKey()
        left_value = self._evaluate_recursive(tree.getLeftTree())
        right_value = self._evaluate_recursive(tree.getRightTree())

        if left_value is None or right_value is None:
            return None

        if operator == '+':
            return left_value + right_value
        elif operator == '-':
            return left_value - right_value
        elif operator == '*':
            return left_value * right_value
        elif operator == '/':
            return left_value / right_value
        elif operator == '**':
            return left_value ** right_value
        else:
            # Assuming it's a variable
            return self._get_variable_value(operator, left_value, right_value)

    def _evaluate_matrix(self, tree):
        matrix_expression = tree.getKey()
        matrix_values = self._parse_matrix_expression(matrix_expression)
        return np.array(matrix_values)

    def _parse_matrix_expression(self, matrix_expression):
        # Remove outer brackets and split by '],[' to get rows
        matrix_str = matrix_expression[2:-2]
        rows = matrix_str.split('],[')

        # Split each row by ',' to get individual values
        matrix_values = [list(map(float, row.split(','))) for row in rows]

        return matrix_values

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

    def _get_variable_value(self, variable, left_value, right_value):
        return self.storage.get(variable, None) or right_value

    def __str__(self):
        return self.expression


# Example usage
if __name__ == '__main__':
    tree = ParseTree('[[1,2],[3,4]] + [[5,6],[7,8]]')
    tree.printInorder(0)
    result = tree.evaluate()
    print(result)
    print(tree)
