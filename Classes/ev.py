from BinaryTree import BinaryTree
from ParseTree import ParseTree

def evaluate(tree):
    leftTree = tree.getLeftTree()
    rightTree = tree.getRightTree()
    op = tree.getKey()
    
    if leftTree is not None and rightTree is not None:
        if op == '+':
            return evaluate(leftTree) + evaluate(rightTree)
        elif op == '-':
            return evaluate(leftTree) - evaluate(rightTree)
        elif op == '*':
            return evaluate(leftTree) * evaluate(rightTree)
        elif op == '/':
            return evaluate(leftTree) / evaluate(rightTree)
    else:
        return float(tree.getKey()) if tree.getKey().replace('.', '', 1).isdigit() else None

def input_equation():
    equation = input("Enter an equation: ")
    return equation

def view_assignments(tree):
    print("Assignments:")
    tree.printPreorder(0)
    print()

def main():
    assignments_tree = None

    while True:
        print("\nOptions:")
        print("1. Input an equation")
        print("2. View current assignments")
        print("3. Exit")

        option = input("Enter option: ")

        if option == '1':
            equation = input_equation()
            parse_tree = ParseTree(equation)
            equation_tree = parse_tree.BuildTree()

            if assignments_tree is None:
                assignments_tree = equation_tree
            else:
                view_assignments(assignments_tree)
                variable = input("Enter a variable for the new assignment: ")
                assignments_tree.insertRight(BinaryTree(variable, None, equation_tree))

        elif option == '2':
            if assignments_tree is not None:
                view_assignments(assignments_tree)
            else:
                print("No assignments yet.")

        elif option == '3':
            print("Exiting program.")
            break

        else:
            print("Invalid option. Please enter a valid option.")

if __name__ == '__main__':
    main()
