import re
from Classes.BinaryTree import BinaryTree
from Classes.Stack import Stack

class ParseTree(BinaryTree):
    def __init__(self, expression, storage=None):
        super().__init__('?')
        self.expression = expression
        self.tokens = re.findall(r'\d+|[a-zA-Z_][a-zA-Z0-9_]*|\+|\-|\*|\/|\*\*|\(|\)', expression)
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

            elif t in ['+', '-', '*', '/']:
                currentTree.setKey(t)
                currentTree.insertRight('?')
                stack.push(currentTree)
                currentTree = currentTree.getRightTree()

            elif t == ')':
                currentTree = stack.pop()

            elif t not in ['+', '-', '*', '/', ')']:
                if t.isdigit():
                    currentTree.setKey(int(t))
    
                else:
                    currentTree.setKey(t)
    
                
                parent = stack.pop()
                currentTree = parent
        return tree

    def evaluate(self):
        return self._evaluate_recursive(self.tree)

    def _evaluate_recursive(self, tree):
        if tree is None:
            return None

        if isinstance(tree.getKey(), int):
            return tree.getKey()

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

    def _get_variable_value(self, variable, left_value, right_value):
        return self.storage.get(variable, None) or right_value
    
    def printPreorder(self, level):
        leftTree = self.tree.getLeftTree()
        rightTree = self.tree.getRightTree()
        print( str(level*'-') + str(self.tree.getKey()))
        if leftTree != None:
            leftTree.printPreorder(level+1)
        if rightTree != None:
            rightTree.printPreorder(level+1)

    #print expression in order of mathematical operations
    def printInorder(self, level):
        leftTree = self.tree.getLeftTree()
        rightTree = self.tree.getRightTree()
        if rightTree != None:
            rightTree.printInorder(level+1)
        print( str(level*'-') + str(self.tree.getKey()))
        if leftTree != None:
            leftTree.printInorder(level+1)

    def __str__(self):
        return self.expression
        

if __name__ == '__main__':
    import re
    from BinaryTree import BinaryTree
    from Stack import Stack
    tree = ParseTree('(5*(1+2))')
    tree.printInorder(0)
    print(tree.evaluate())
    print(tree)