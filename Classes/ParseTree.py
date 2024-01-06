import re
from BinaryTree import BinaryTree
from Stack import Stack

class ParseTree(BinaryTree):
    def __init__(self, expression, storage=None):
        super().__init__(expression)
        self.tokens = re.findall(r'\d+|[a-zA-Z_][a-zA-Z0-9_]*|\+|\-|\*|\/|\*\*|\(|\)', expression)
        self.current_index = 0
        self.storage = storage or {}

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
            elif t in ['+', '-', '*', '/']:
                currentTree.setKey(t)
                currentTree.insertRight('?')
                stack.push(currentTree)
                currentTree = currentTree.getRightTree()
            elif t == ')':
                currentTree = stack.pop()
            elif t not in ['+', '-', '*', '/', ')']:
                # Check if it's a numeric value or a variable
                if t.isdigit():
                    currentTree.setKey(int(t))
                else:
                    currentTree.setKey(t)
                
                parent = stack.pop()
                currentTree = parent

        return tree

    def evaluate(self):
        return self._evaluate_recursive(self.build())

    def _evaluate_recursive(self, node):
        if node is None:
            return None

        if isinstance(node.getKey(), int):
            return node.getKey()  # Numeric value, return as is

        operator = node.getKey()
        left_value = self._evaluate_recursive(node.getLeftTree())
        right_value = self._evaluate_recursive(node.getRightTree())

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
            return self.storage.get(operator)

