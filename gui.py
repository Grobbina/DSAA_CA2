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
        self.safety = True

        while True:
            print("Please select your choice (1,2,3,4,5,6):\n \t1. Add/Modify assignment statement\n \t2. Display Current Assignment Statement\n \t3. Evaluate a Single Variable\n \t4. Read Assignment statements from file\n \t5. Sort assignment statemnets\n \t6. Linear Equations\n \t7. Exit\n")

            num = int(input("Enter choice:"))

            if num <= 0 or num > 7:
                print("Please choose a valid option\n")
            elif num == 1:
                statement = input("Please enter assignment statement you want to add/modify:\nFor example, a=(1+2)\n")
                var, statement = statement.split('=' , 1)
                tree = ParseTree(statement)
                self.storage[var] = tree
                #check variable for coefficients
                pattern = re.compile(r'([+-]?\d*)[a-zA-Z]')
                # Find all matches in the string
                matches = pattern.findall(var)
                if matches[0] != '':
                    var, statement = self.simplifyevaluation(var, tree)
                    #add the simplified equation to the storage
                    self.storage[var] = statement
                input("\n Press enter key to continue...")

            elif num == 2:
                print("\nCurrent Assignments:")
                for var, parsed_tree in self.storage.items():
                    original = parsed_tree
                    parsed_tree = self.evaluateexpressions({var: parsed_tree})
                    if parsed_tree is not None:
                        print(f'{var}={original}-->{parsed_tree.evaluate()}\n')
                    else:
                        print(f'{var}={original}-->None\n')
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
                output_name = input("Enter the output name: ")
                self.sort_assignment_statements(output_name)

            elif num == 6:
                print('Turning safety mode on will prevent you from evaluating cross referenced variables in linear equations\n Turning safety mode off will allow you to evaluate cross referenced variables in linear equations\n')
                status = 'OFF' if self.safety else 'ON'
                while self.safety not in ['y','n',True,False]:
                    self.safety = input(f"Toggle safety mode {status}? (y/n): ")
                if self.safety == 'y':
                    if status == 'ON':
                        self.safety = True
                    else:
                        self.safety = False
                else:
                    pass
            elif num == 7:
                print('\nBye, thanks for using ST150/DSAA Assignment Statements Evaluation & Sorter')
                break

    def sort_assignment_statements(self, output_name):
        sorted_statements = {}

        for var, parsed_tree in self.storage.items():
            original = parsed_tree
            parsed_tree = self.evaluateexpressions({var: parsed_tree})
            value = parsed_tree.evaluate() if parsed_tree is not None else 'None'

            if value not in sorted_statements:
                sorted_statements[value] = []

            sorted_statements[value].append(f'{var}={original}')

        with open(output_name, 'w') as output_file:
            for value, statements in sorted_statements.items():
                output_file.write(f'*** Statements with value => {value}\n')
                for statement in statements:
                    output_file.write(f'{statement}\n')

        print(f"Sorted content has been written to {output_name}")


    #converts expressions to its lowest level form (no vars all numbers)
    def evaluateexpressions(self, dict, level=0):
<<<<<<< Updated upstream
        if level >len(list(self.storage.keys())):
            print('\nCannot evaluate, error:Reference loop')
            return None
=======
>>>>>>> Stashed changes

        #prevent infinite loop
        if self.safety:
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
                        print(parsed_tree_new)
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
            
        else:
            #try to solve linear equations using substitution
            var = list(dict.keys())[0]
            parsed_tree = dict[var]
            parsed_tree_str = str(parsed_tree)
            #move all variables to left side and all numbers to right side
            match = re.search(r'[a-zA-Z]+', parsed_tree_str)
            #check if the match is the same variable as the one we are trying to solve
            if match and match.group() == var:
                variable = match.group()
                #find the coefficient of the variables in the expression

                pattern = re.compile(r'([+-]?\d*)[a-zA-Z]')
                matches = pattern.findall(parsed_tree_str)
                coefficients = [int(match) if match else 1 for match in matches]


                for match in matches:
                    equation_str = parsed_tree.replace(match, '')

                # remove the variable itself from the string
                equation_str = re.sub(r'[a-zA-Z]', '', equation_str)



            
            elif match:
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
            

    def simplifyevaluation(self, var, parsed_tree):
        #check var for coefficients
        pattern = re.compile(r'([+-]?\d*)[a-zA-Z]')
        # Find all matches in the string
        matches = pattern.findall(var)
        # Remove the variables and their coefficients from the string
        for match in matches:
            new_var = var.replace(match, '')

        #add all the coefficients together
        coefficient = 0
        for match in matches:
            coefficient += int(match)
        #remove the variable itself from the string
        equation_str = str(parsed_tree)
        #divide the equation by the coefficient(add a /8 to the end of the equation)
        equation_str = f'({equation_str}/{coefficient})'
        #parse the equation
        print(equation_str)
        parsed_tree = ParseTree(equation_str)
        return new_var, parsed_tree


if __name__ == '__main__':
    gui = Gui()
