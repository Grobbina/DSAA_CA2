import re
from Classes.BinaryTree import BinaryTree
from Classes.Stack import Stack

class ParseTree(BinaryTree):
    def __init__(self, expression, storage=None):
        super().__init__('?')
        self.expression = expression
        # Use a more specific pattern for '**' to ensure it is treated as a single token
        self.tokens = re.findall(r'\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|\*\*|[+\-*/()]', expression)
        #if tokens are number followed by variable, add a * between them
        for i in range(len(self.tokens)-1):
            if self.tokens[i].isnumeric() and self.tokens[i+1].isalpha():
                self.tokens.insert(i+1, '*')
                #insert brackets as well 
                self.tokens.insert(i, '(')
                self.tokens.insert(i+4, ')')
        #if number is followed by opening bracket add a * between them
        for i in range(len(self.tokens)-1):
            if self.tokens[i].isnumeric() and self.tokens[i+1] == '(':
                self.tokens.insert(i+1, '*')
        
        #check for negatives 
        for i in range(len(self.tokens)-1):
            if self.tokens[i] in ['*', '/', '+', '-', '(',')'] and self.tokens[i+1] == '-':
                del self.tokens[i+1]
                self.tokens[i+2] = f'-{self.tokens[i+2]}'
        print(self.tokens)
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

            elif t not in ['+', '-', '*', '/', ')','**']:
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
    tree = ParseTree('(0+3((20-(2(0+0)))/3.0))')
    tree.printInorder(0)
    print(tree.evaluate())
    print(tree)