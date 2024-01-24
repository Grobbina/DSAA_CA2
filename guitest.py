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
        self.values = {}
        self.lin = {}
        self.safety = True

        while True:
            print("Please select your choice (1,2,3,4,5,6):\n \t1. Add/Modify assignment statement\n \t2. Display Current Assignment Statement\n \t3. Evaluate a Single Variable\n \t4. Read Assignment statements from file\n \t5. Sort assignment statemnets\n \t6. Linear Equations\n \t7. Exit\n")
            solution = []
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
                print(self.storage)
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
                equation = input('Welcome to the Linear Equation Solver, please enter the first equation:\n')
                variables = re.findall(r'[a-zA-Z]+', equation)
                variables = list(set(variables))
                var, statement = equation.split('=' , 1)
                self.LinearEquation(var, statement, variables)
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
            if self.safety:
                print('\nCannot evaluate, error:Reference loop')
                return None
            else:
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
                        #if it is, we use another variable to store the equation
                        match = re.search('([+-]?\d*)[0-9]*[a-zA-Z]+', tomove)
                        tokeep = match.group()
                        tomove = var.replace(tokeep, '')
                    else:
                        break
                #add a 0 to the front of the equation
                #move to the right side of the equation
                if tomove[0] == '+':
                    tomove = tomove.replace('+', '')
                statement = f'{statement}-{tomove}'
                #evaluate the 'numeric' part of the equation
                #extract only numerics not followed by a letter but following a + or - sign
                matchno = re.findall(r'(\+?-?\d+(?![a-zA-Z]))', statement)
                evaluated = sum([int(i) for i in matchno])
                #redefine the statement with the evaluated numerics
                #remove the numerics used in the evaluation
                statement = re.sub(r'(\+?-?\d+(?![a-zA-Z]))', '', statement)

                statement = f'{evaluated}+{statement}'
                return tokeep, statement
            
    def checkstat(self, var, statement):
        pattern = re.compile(r'[a-zA-Z]+')
        statcheck = pattern.findall(statement)
        #check that statecheck length is 0
        if len(statcheck) == 0:
            return var, statement
        else:
            #we move all the variables to var
            #find all the variables on the right, this regex pattern will get all variables as well as their co efficient and sign
            tobemoved = re.findall(r'([-+]?\s*\d*\s*[a-zA-Z])', statement)
            #remove all the variables from the statement
            statement = re.sub(r'([-+]?\s*\d*\s*[a-zA-Z])', '', statement)
            tobemoved = ''.join(tobemoved)
            #if the first chraacter is not a symbol, add a + to the front
            if tobemoved[0] not in ['+', '-']:
                tobemoved = f'+{tobemoved}'
            #change all the + to - and vice versa
            tobemoved = tobemoved.replace('+', '!')
            tobemoved = tobemoved.replace('-', '+')
            tobemoved = tobemoved.replace('!', '-')
            #add the variables to var
            var = f'{var}{tobemoved}'
            #add of all the co efficients in var and simplify the statement
            #get all the variables in var
            variables = re.findall(r'[a-zA-Z]+', var)
            new_var = ''
            #remove duplicates
            variables = list(set(variables))
            for v in variables:
                #get all the co efficients of the variable
                co_efficients = re.findall(rf'([-+]?\s*\d*)\s*{v}', var)
                print(co_efficients)
                #add all the co efficients
                total = 0
                for c in co_efficients:
                    if c == '' or c == '+':
                        c = 1
                    elif c == '-':
                        c = -1
                    total += int(c)
                #replace all the co efficients with the total
                new_var += f'{total}{v}'
            return new_var, statement


    def LinearEquation(self, var, statement, varlist):
        equation2 = input('Linear equation detected, please enter the second equation:\n')
        var2, statement2 = equation2.split('=' , 1)
        #check if the variables in the 2 equations are the same
        varlist2 = re.findall(r'[a-zA-Z]+', var2)
        varlist2 = list(set(varlist2))
        if varlist != varlist2:
            print('Cannot solve linear equations, The inputted variables are not the same')
            return
        #store the 2nd equation into the storage
        tree = ParseTree(statement2)
        self.storage[var2] = tree
        #try to solve the equation using numpy
        import numpy as np
        #convert the equations into the "standard" linear equation form
        pattern = re.compile(r'[a-zA-Z]+')
        var, statement = self.checkstat(var, statement)
        var2, statement2 = self.checkstat(var2, statement2)

        #convert these equations into numpy arrays
        #get all the variables in the equation
        variables = re.findall(r'[a-zA-Z]+', var)
        nparray = []
        for i in [var, var2]:
            temp = []
            for v in variables:
                #get all the co efficients of the variable
                co_efficients = re.findall(rf'([-+]?\s*\d*)\s*{v}', i)
                for c in co_efficients:
                    if c == '' or c == '+':
                        c = 1
                    elif c == '-':
                        c = -1
                    temp.append(int(c))
            nparray.append(temp)
        #convert the equations into numpy arrays
        nparray = np.array(nparray)
        rhs = np.array([int(statement), int(statement2)])
        #solve the equations
        try:
            solution = np.linalg.solve(nparray, rhs)
            st = ''
            for i in range(len(solution)):
                st += f'{variables[i]} = {round(solution[i], 2)}\t'
            print(st)
            choice = ''
            while choice not in ['y','n']:
                choice = input('Do you want to save the solution?(y/n)\n: ')
                if choice == 'y':
                    for i in range(len(solution)):
                        self.storage[variables[i]] = ParseTree(f'{solution[i]}')
                else:
                    pass
        except:
            print('Cannot solve linear equations')
            pass

if __name__ == '__main__':
    gui = Gui()
