class BinaryTree:
    def __init__(self,key, leftTree = None, rightTree = None):
        self.key = key
        self.leftTree = leftTree
        self.rightTree = rightTree
    def setKey(self, key):
        self.key = key
    def getKey(self):
        return self.key
    def getLeftTree(self):
        return self.leftTree
    def getRightTree(self):
        return self.rightTree 
    def insertLeft(self, newNode):
        if self.leftTree == None:
            self.leftTree = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.leftTree = self.leftTree
            self.leftTree = t
    def insertRight(self, newNode):
        if self.rightTree == None:
            self.rightTree = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightTree = self.rightTree
            self.rightTree = t
    def printPreorder(self, level):
        print( str(level*'-') + str(self.key))
        if self.leftTree != None:
            self.leftTree.printPreorder(level+1)
        if self.rightTree != None:
            self.rightTree.printPreorder(level+1)

    def printInorder(self, level):
        if self.leftTree != None:
            self.leftTree.printInorder(level+1)
        print( str(level*'-') + str(self.key))
        if self.rightTree != None:
            self.rightTree.printInorder(level+1)

    def __str__(self):
        return str(self.key)
    

if __name__ == '__main__':
    leftTree = BinaryTree('Chapter 1',
    BinaryTree('Section 1.1'),
    BinaryTree('Section 1.2',
    BinaryTree('Section 1.2.1'),None))
    rightTree = BinaryTree('Chapter 2',
    BinaryTree('Section 2.1'),
    BinaryTree('Section 2.2',
    BinaryTree('Section 2.2.1'),
    BinaryTree('Section 2.2.2')) )
    tree = BinaryTree('Contents', leftTree, rightTree)
    tree.printPreorder(0)