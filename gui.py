from Classes.ParseTree import ParseTree
from Classes.Stack import Stack 
import re
from Classes.BinaryTree import BinaryTree

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
                var, statement = statement.split('=' , 1)
                tree = ParseTree(statement)
                self.storage[var] = tree
                input("\n Press enter key to continue...")

            elif num == 2:
                print("\nCurrent Assignments:")
                for var, parsed_tree in self.storage.items():
                    original = parsed_tree
                    parsed_tree = self.evaluateexpressions({var: parsed_tree})
                    if parsed_tree is not None:
                        print(f'{var}={original}-->{parsed_tree.evaluate()}')
                    else:
                        print(f'{var}={original}-->None')
            elif num == 3:
                evaloption = input("Please enter variable you want to evaluate:\n")
                print('\nExpression Tree:')
                if evaloption in self.storage:
                    parsed_tree = self.storage[evaloption]
                    parsed_tree = self.evaluateexpressions({evaloption: parsed_tree})
                    value = parsed_tree.evaluate()
                    parsed_tree.printInorder(0)
                    print(f'Value for "{evaloption}" is {value}')
                else:
                    print(f"{evaloption}-->None")
            elif num == 4:
                filepath = input("Please enter the input file: ")
                with open(filepath) as fp:
                    line = fp.readline()
                    while line:
                        line = line.rstrip()
                        #split the line into variable and statement using '='
                        var, statement = line.split('=' , 1)
                        tree = ParseTree(statement)
                        self.storage[var] = tree
                        line = fp.readline()
                print('CURRENT ASSIGNMENTS:')
                print('*'*10)
                self.storage = dict(sorted(self.storage.items(), key=lambda key: key[0]))
                for var, parsed_tree in self.storage.items():
                    original = parsed_tree
                    parsed_tree = self.evaluateexpressions({var: parsed_tree})
                    if parsed_tree is not None:
                        print(f'{var}={original}-->{parsed_tree.evaluate()}')
                    else:
                        print(f'{var}={original}-->None')
                    
                input('\nPress enter key, to continue...')

            elif num == 5:
                print(5)
            elif num == 6:
                print('\nBye, thanks for using ST150/DSAA Assignment Statements Evaluation & Sorter')
                break

    #converts expressions to its lowest level form (no vars all numbers)
    def evaluateexpressions(self, dict, level=0):
        if level >len(list(self.storage.keys())):
            print('Cannot evaluate, error:Reference loop')
            return None

        var = list(dict.keys())[0]
        parsed_tree = dict[var]
        if parsed_tree.evaluate() is None:
            parsed_tree_str = str(parsed_tree)
            #find all "words" in the expression (variables)
            match = re.search(r'[a-zA-Z]+', parsed_tree_str)
            if match:
                variable = match.group()
                if variable in self.storage:
                    parsed_tree_str = parsed_tree_str.replace(variable, str(self.storage[variable]))
                    parsed_tree_new = ParseTree(parsed_tree_str)
                    #check whether there are more variables to replace
                    match = re.search(r'[a-zA-Z]+', parsed_tree_str)
                    if match:
                        return self.evaluateexpressions({var: parsed_tree_new},level+1)
                    else:
                        return parsed_tree_new
                
                #referenced var doesnt exist, just return None
                else:
                    return None
        else:
            return parsed_tree
    

if __name__ == '__main__':
    gui = Gui()
