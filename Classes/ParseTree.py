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

            


if __name__ == '__main__':
    tree = ParseTree('(3+5)')

    tree.build()

    