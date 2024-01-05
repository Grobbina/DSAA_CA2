import regex as re
from BinaryTree import BinaryTree
from Stack import Stack

class ParseTree(BinaryTree):
    def __init__(self, expression):
        self.expression = expression
        self.tokens = re.findall(r'\d+|\+|\-|\*|\/|\*\*|\(|\)', expression)
        self.current_index = 0

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
            elif t not in ['+', '-', '*', '/', ')'] :
                currentTree.setKey(int(t))
                parent = stack.pop()
                currentTree = parent
            elif t == ')':
                currentTree = stack.pop()
            else:
                raise ValueError
                return tree

        def evaluate(self, tree): #evaluation
            leftTree = tree.getLeftTree()
            rightTree = tree.getRightTree()
            op = tree.getKey()
            
            if leftTree is not None and rightTree is not None:
                if op == '+':
                    return self.evaluate(leftTree) + self.evaluate(rightTree)
                elif op == '-':
                    return self.evaluate(leftTree) - self.evaluate(rightTree)
                elif op == '*':
                    return self.evaluate(leftTree) * self.evaluate(rightTree)
                elif op == '/':
                    return self.evaluate(leftTree) / self.evaluate(rightTree)
            else:
                return float(tree.getKey()) if str(tree.getKey()).replace('.', '', 1).isdigit() else None    


if __name__ == '__main__':
    tree = ParseTree('(3+5)')

    tree.build()

    