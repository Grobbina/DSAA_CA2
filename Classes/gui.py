from ParseTree import ParseTree
from Stack import Stack 
import regex as re
from BinaryTree import BinaryTree

def starty():
    input("""
    ******************************************************
    * ST1507 DSAA: Welcomme to:                          *
    * ~Evaluating and sorting assignment statements ~    *
    *----------------------------------------------------*
    *                                                    *
    * - Done by: Sean See(2214311),Cai Ruizhe(2214535)   *
    * - Class: DAAA/2B01                                 *
    ******************************************************

    Press Enter to continue...
    """)
starty()

#Main Gui
class Gui:
    def __init__(self):
        self.storage = {}


        while True:
            print(f"Please select your choice (1,2,3,4,5,6):\n \t1. Add/Modify assignment statement\n \t2. Display Current Assignment Statement\n \t3. Evaluate a Single Variable\n \t4. Read Assignment statements from file\n \t5. Sort assignment statemnets\n \t6. Exit")
        
            num = int(input("Enter choice:"))

            if num <= 0 or num > 6:
                print("Please choose a valid option\n")
            elif num == 1:
                statement = input("Please enter assignment statement you want to add/modify:\nFor example, a=(1+2)\n")
                #find the variable name
                var = statement[0]
                #cut out the variable name and the equal sign
                statement = statement[2:]
                #create a parse tree
                tree = ParseTree(statement)
                #build the tree
                tree.build()
                #save the tree into a dictionary
                self.storage[var] = tree
                input("\n Press enter key to continue...")


            elif num == 2:
                print("Current Assignment Statements:")
                for key in self.storage:
                    print(f"{key} = {self.storage[key].expression}")
                
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