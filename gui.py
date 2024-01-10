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
                pattern = re.compile(r'([+-]?\d*)[a-zA-Z]+')
                # Find all matches in the string
                matches = pattern.findall(var)

                #check if there are coefficients in the variable, if there is we try to process it to be something like 1var = equation
                if matches[0] != '':
                    #check if there is only 1 variable in the left side of the equation

                    if len(matches) != 1:
                        #if there are more than 1 variable in the left side of the equation, we try to process it to be something like 1var = equation
                        var, statement = self.VarExtraction(var, statement, len(matches))
                        tree = ParseTree(f'({statement})')
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
                print('Turning safety mode on will prevent you from evaluating cross referenced variables in linear equations\nTurning safety mode off will allow you to evaluate cross referenced variables in linear equations\n')
                status = 'OFF' if self.safety else 'ON'
                self.safety = input(f"Toggle safety mode {status}? (y/n): ")
                while self.safety not in ['y','n',True,False]:
                    self.safety = input(f"INVALID OPTION\nToggle safety mode {status}? (y/n): ")
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
        if level >len(list(self.storage.keys())):
            print('\nCannot evaluate, error:Reference loop')
            return None

        var = list(dict.keys())[0]
        parsed_tree = dict[var]
        if parsed_tree.evaluate() is None:
            if self.safety == False:
                var, parsed_tree = self.unsafeevaluation(var, parsed_tree)
                print(var, parsed_tree)
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
        else:
            return parsed_tree
            

    def simplifyevaluation(self, var, parsed_tree):
        #check var for coefficients
        pattern = re.compile(r'([+-]?\d*\.?\d+)?[a-zA-Z]+')
        # Find all matches in the string
        matches = pattern.findall(var)
        # Remove the variables and their coefficients from the string
        for match in matches:
            new_var = var.replace(match, '')

        #add all the coefficients together
        coefficient = 0
        for match in matches:
            if match == '':
                match = '0'
            coefficient += float(match)

        #remove the variable itself from the string
        equation_str = str(parsed_tree)
        #divide the equation by the coefficient(add a /8 to the end of the equation)
        equation_str = f'({equation_str}/{coefficient})'
        #parse the equation
        parsed_tree = ParseTree(equation_str)
        return new_var, parsed_tree
    
    
    def unsafeevaluation(self, var, parsed_tree):
        parsed_tree_str = str(parsed_tree)
        #find all "words" in the expression (variables)
        match = re.findall(r'[a-zA-Z]+', parsed_tree_str)
        if len(match) == 1 and match[0] == var:
            #find the coefficient of the variables in the expression
            pattern = re.compile(r'([+-]?\d*)[a-zA-Z]+')
            matches = pattern.findall(parsed_tree_str)

            #remove coefficients from the equation before transforming them
            # for match in matches:
            #     equation_str = parsed_tree_str.replace(match, '')
            
            #fix the coefficients eg no coefficient = 1, - = -1
            for i in range(len(matches)):
                if matches[i] == '':
                    matches[i] = '1'
                elif matches[i] == '-':
                    matches[i] = '-1'
            coefficients = [float(match) if match else 1 for match in matches]
            #remove the coefficients from the equation
            print(coefficients)
            for match in matches:
                #remove the + and - from the coefficient
                onlynumber = re.search('\d+', match)
                match = onlynumber.group()
                temp = parsed_tree_str.replace(f'{match}{var}', var)
            print('replace' , parsed_tree_str)
            temptree = ParseTree(temp)
            #add a part here to find all * and / modifiers for each coefficient and resolve them
            #OK (LOL i am the one who wrote both of these comments )
            print(temptree)
            tokens = temptree.tokens
            match = re.findall(r'([*/])', parsed_tree_str)
            for i in range(len(tokens)-1):
                previousoperator = ''
                if tokens[i] in ['+', '-']:
                    previousoperator = tokens[i]
                if tokens[i] in ['*', '/']:
                    if tokens[i] == '*':
                        #check for coefficient of token
                        if previousoperator == '-' :
                            multiplier = float(f'-{tokens[i-1]}')
                        else:
                            multiplier = tokens[i-1]
                        print(f'Multiplying {coefficients} by {multiplier}')
                        coefficients = list(map(lambda x: x * float(multiplier), coefficients))
                    elif tokens[i] == '/':
                        if previousoperator == '-':
                            multiplier = float(f'-{tokens[i+2]}')
                        else:
                            multiplier = tokens[i+1]
                        print(f'Dividing {coefficients} by {multiplier}')
                        coefficients = list(map(lambda x: x / float(multiplier), coefficients))
            print(coefficients)


            #remove variables itself from the equation

            parsed_tree_str = re.sub(r'[a-zA-Z]+', '(0+0)', parsed_tree_str)
            
            #set the new tree to the simplified equation
            parsed_tree = ParseTree(parsed_tree_str)
            
            #sum up equations and get the total coefficient
            total = 0
            for coefficient in coefficients:
                total += float(coefficient)

            #check left var for coefficients and simplify
            var_coeff = re.search(r'([+-]?\d*)[a-zA-Z]+', var)
            if var_coeff.group(1) != '':
                var = var.replace(var_coeff.group(1), '')
                var = f'{total + float(var_coeff.group(1))}{var}'
                var, parsed_tree = self.simplifyevaluation(var, parsed_tree)
                return var, parsed_tree
            else:
                var = f'{1+total}{var}'
                print(var, parsed_tree)
                print(parsed_tree)
                var, parsed_tree = self.simplifyevaluation(var, parsed_tree)
                return var, parsed_tree
        else:
            return var, parsed_tree
    

    def VarExtraction(self, var, statement, no_Of_Vars=0):
        #find all "words" in the var side of the equation (variables)
        match = re.findall(r'[a-zA-Z]+', var)
        #if there is only 1 variable in the var side of the equation
        if len(match) == 1:
            return var, statement
        else:
            for i in range(no_Of_Vars-1):
                match = re.search('([+-]?\d*)[0-9]*[a-zA-Z]+', var)
                tokeep = match.group()
                tomove = var.replace(tokeep, '')
                #check if the variables are already in the storage, if it is, we use another variable to store the equation, 
                #if all variables are, replace the last variable in storage with the equation
                for i in range(no_Of_Vars-1):
                    #check if tokeep is already in storage
                    match = re.search(r'[a-zA-Z]+', tokeep)
                    if match.group() in self.storage:
                        print('finding new variable')
                        #if it is, we use another variable to store the equation
                        match = re.search('([+-]?\d*)[0-9]*[a-zA-Z]+', tomove)
                        tokeep = match.group()
                        print('Using', tokeep, 'to store equation')
                        tomove = var.replace(tokeep, '')
                    else:
                        break
                #add a 0 to the front of the equation
                if tomove[0] in ['+', '-']:
                    tomove = f'0{tomove}'
                #move to the right side of the equation
                statement = f'{statement}-({tomove})'
                return tokeep, statement

if __name__ == '__main__':
    gui = Gui()
