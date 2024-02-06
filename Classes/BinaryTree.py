class BinaryTree:
    # Initializing the Binary Tree with a key and optional left and right subtrees
    def __init__(self, key, leftTree=None, rightTree=None):
        self.key = key
        self.leftTree = leftTree
        self.rightTree = rightTree
    
    # Method to set the key of the node
    def setKey(self, key):
        self.key = key
    
    # Method to get the key of the node
    def getKey(self):
        return self.key
    
    # Method to get the left subtree
    def getLeftTree(self):
        return self.leftTree
    
    # Method to get the right subtree
    def getRightTree(self):
        return self.rightTree 
    
    # Method to insert a new node as the left child
    def insertLeft(self, newNode):
        if self.leftTree == None:
            self.leftTree = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.leftTree = self.leftTree
            self.leftTree = t
    
    # Method to insert a new node as the right child
    def insertRight(self, newNode):
        if self.rightTree == None:
            self.rightTree = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightTree = self.rightTree
            self.rightTree = t
    
    # Method to print the tree in preorder traversal
    def printPreorder(self, level):
        print(str(level * '-') + str(self.key))
        if self.leftTree != None:
            self.leftTree.printPreorder(level + 1)
        if self.rightTree != None:
            self.rightTree.printPreorder(level + 1)
    
    # Method to print the tree in inorder traversal
    def printInorder(self, level):
        if self.rightTree != None:
            self.rightTree.printInorder(level + 1)
        print(str(level * '-') + str(self.key))
        if self.leftTree != None:
            self.leftTree.printInorder(level + 1)
    
    # Method to represent the node as a string
    def __str__(self):
        return str(self.key)


if __name__ == '__main__':
    # Creating left subtree
    leftTree = BinaryTree('Chapter 1',
                          BinaryTree('Section 1.1'),
                          BinaryTree('Section 1.2',
                                     BinaryTree('Section 1.2.1'),
                                     None))
    
    # Creating right subtree
    rightTree = BinaryTree('Chapter 2',
                           BinaryTree('Section 2.1'),
                           BinaryTree('Section 2.2',
                                      BinaryTree('Section 2.2.1'),
                                      BinaryTree('Section 2.2.2')))
    
    # Creating the main tree with contents
    tree = BinaryTree('Contents', leftTree, rightTree)
    
    # Printing the preorder traversal of the tree
    tree.printPreorder(0)
    # print(tree.strPreorder()) # Uncommented since strPreorder is not defined
