from ParseTree import ParseTree
from Stack import Stack 
import regex as re
from BinaryTree import BinaryTree

def starty():
    input("""
    ******************************************************
    * ST1507 DSAA: Welcomme to:                          *
    * ~Evaluating and sorting assignment statements ~    *
    ----------------------------------------------------
    *                                                    *
    * - Done by: Sean See(2214311),Cai Ruizhe(2214535)   *
    * - Class: DAAA/2B01                                 *
    ******************************************************

    Press Enter to continue...
    """)
starty()

#Main Gui
from ParseTree import ParseTree
from Stack import Stack

class Gui:
    def __init__(self):
        self.storage = {}

        while True:
            print("Please select your choice (1,2,3,4,5,6):\n \t1. Add/Modify assignment statement\n \t2. Display Current Assignment Statement\n \t3. Evaluate a Single Variable\n \t4. Read Assignment statements from file\n \t5. Sort assignment statemnets\n \t6. Exit")

            num = int(input("Enter choice:"))

            if num <= 0 or num > 6:
                print("Please choose a valid option\n")
            elif num == 1:
                statement = input("Please enter assignment statement you want to add/modify:\nFor example, a=(1+2)\n")
                var = statement[0]
                statement = statement[2:]
                tree = ParseTree(statement)
                tree.build()
                self.storage[var] = tree
                input("\n Press enter key to continue...")

            elif num == 2:
                print("\nCurrent Assignments:")
                for var, parsed_tree in self.storage.items():
                    print(f"{var}={parsed_tree}-->{parsed_tree.evaluate()}")

            elif num == 3:
                print(3)
            elif num == 4:
                print(4)
            elif num == 5:
                print(5)
            elif num == 6:
                print('\nBye, thanks for using ST150/DSAA Assignment Statements Evaluation & Sorter')
                break

if __name__ == '__main__':
    gui = Gui()
