import re
import turtle
import numpy as np
from Classes.BinaryTree import BinaryTree
from Classes.Stack import Stack

class MatrixOperations(BinaryTree):
    def __init__(self, expression, storage=None):
        super().__init__('?')
        self.expression = expression
        self.tokens = re.findall(r'\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|\*\*|[+\-*/()\[\],]+|\[\[.*?\]\]', expression)

        loop = len(self.tokens)-1
        i = 0
        while loop > 0:
            if self.tokens[i] in ['*', '/', '(',')'] and self.tokens[i+1] == '-':
                if self.is_digit_neg(self.tokens[i+2]):
                    del self.tokens[i+1]
                    loop -=1
                    self.tokens[i+1] = f'-{self.tokens[i+1]}'
                else:
                    self.tokens[i+1] = f'-1'
                    self.tokens.insert(i+2, '*')
                    loop +=1
            loop -=1
            i +=1

            if self.tokens[i] == '-' and self.tokens[i+1] == '-':
                del self.tokens[i]
                self.tokens[i] = '+'
                loop -=1
            if self.tokens[i] == '+' and self.tokens[i+1] == '-':
                del self.tokens[i]
                loop -=1

        for i in range(len(self.tokens)-1):
            if self.is_digit_neg(self.tokens[i]) and self.tokens[i+1].isalpha():
                self.tokens.insert(i+1, '*')
                self.tokens.insert(i, '(')
                self.tokens.insert(i+4, ')')

        for i in range(len(self.tokens)-1):
            if self.is_digit_neg(self.tokens[i]) and self.tokens[i+1] == '(':
                self.tokens.insert(i+1, '*')

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
            elif t == '[':
                currentTree.insertLeft('?')
                stack.push(currentTree)
                currentTree = currentTree.getLeftTree()

            elif t == ']':
                currentTree = stack.pop()

            elif ',':
                currentTree.setKey(',')
                currentTree.insertRight('?')
                stack.push(currentTree)
                currentTree = currentTree.getRightTree()

            elif t not in ['+', '-', '*', '/', ')','**']:
                if t.isalpha():
                    currentTree.setKey(t)
                elif t.startswith("[[") and t.endswith("]]"):
                    currentTree.setKey(self._parse_matrix(t))
                else:
                    currentTree.setKey(float(t))

                parent = stack.pop()
                currentTree = parent
        return tree

    def _parse_matrix(self, matrix_str):
        matrix_str = matrix_str[2:-2]
        rows = matrix_str.split("],[")

        matrix = []
        for row in rows:
            elements = row.split(",")
            matrix.append([float(e) for e in elements])

        return np.array(matrix)

    def evaluate(self):
        return self._evaluate_recursive(self.tree)

    def _evaluate_recursive(self, tree):
        if tree is None:
            return None

        if isinstance(tree.getKey(), float):
            return tree.getKey()
        elif isinstance(tree.getKey(), np.ndarray):
            return tree.getKey()

        operator = tree.getKey()
        left_value = self._evaluate_recursive(tree.getLeftTree())
        right_value = self._evaluate_recursive(tree.getRightTree())

        if left_value is None or right_value is None:
            return None
    
        if operator == '+':
            return np.add(left_value, right_value)
        elif operator == '-':
            return np.subtract(left_value, right_value)
        elif operator == '*':
            return np.dot(left_value, right_value)
        elif operator == '/':
            return np.divide(left_value, right_value)
        elif operator == '**':
            return np.power(left_value, right_value)
        else:
            return self._get_variable_value(operator, left_value, right_value)

    def _get_variable_value(self, variable, left_value, right_value):
        return self.storage.get(variable, None) or right_value

    def printInorder(self, level):
        leftTree = self.tree.getLeftTree()
        rightTree = self.tree.getRightTree()
        if rightTree != None:
            rightTree.printInorder(level+1)
        print( str(level*'-') + str(self.tree.getKey()))
        if leftTree != None:
            leftTree.printInorder(level+1)

    def is_digit_neg(self, n: str) -> bool:
        try:
            int(n)
            return True
        except ValueError:
            return False

    def __str__(self):
        return self.expression

if __name__ == '__main__':
    tree = ParseTree('[[1,2],[3,4]]+[[5,6],[7,8]]')
    tree.printInorder(0)
    print(tree.evaluate())
    print(tree)
