from Classes.ParseTree import ParseTree
from Classes.Stack import Stack 
import re
from Classes.BinaryTree import BinaryTree
import turtle
#from Classes.MatrixOperations import MatrixOperations
from Classes.validation import validator
from Classes.MatrixOperations import MatrixOperation
validator = validator()

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
            print("Please select your choice (1,2,3,4,5,6):\n \t1. Add/Modify assignment statement\n \t2. Display Current Assignment Statement\n \t3. Evaluate a Single Variable\n \t4. Read Assignment statements from file\n \t5. Sort assignment statemnets\n \t6. Simultaneous Equations\n \t7. Turtle draw parseTree\n \t8. Perform Matrix or Column Vector Operations\n \t9. Toggle Auto Simplification \n\t10. Exit\n")
            solution = []
            num = input("Enter choice:")
            if num.isdigit():
                num = int(num)
            else:
                print("Please choose a valid option\n")
                continue
            if num <= 0 or num > 10:
                print("Please choose a valid option\n")
            

            
            elif num == 1:
                passed = False
                while passed != True:
                    statement = input("Please enter assignment statement you want to add/modify:\nFor example, a=(1+2)\n")
                    try:
                        var, statement = statement.split('=' , 1)
                    except:
                        print("Invalid input, please re-enter\n")
                        continue
                    if len(var) == 0 or len(statement) <= 3 or (statement[0] == '(' and statement[-1] == ')') == False:
                        print("Invalid input, please re-enter\n")
                        continue
                    else:
                        passed = True
                tree = ParseTree(statement)
                self.storage[var] = tree
                #check variable for coefficients
                pattern = re.compile(r'([+-]?\d*)[a-zA-Z]+')
                # Find all matches in the string
                matches = pattern.findall(var)

                #check if there are coefficients in the variable, if there is we try to process it to be something like 1var = equation
                if matches[0] != '' and self.safety == False:
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
                input("\n Press enter key to continue...")
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
                filepath = validator.addtxt(filepath)
                while validator.filevalidation(filepath):
                    filepath = input("Please enter the input file: ")
                    filepath = validator.addtxt(filepath)
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
                while True:
                    equation = input('\n\nWelcome to the Simultaneous Equation Solver, please enter the first equation:\n')
                    variables = re.findall(r'[a-zA-Z]+', equation)
                    variables = list(set(variables))
                    try:
                        var, statement = equation.split('=' , 1)
                        break
                    except:
                        print('Invalid input, please re-enter')
                        continue
                self.SimultaneousEquation(var, statement, variables)

            elif num == 7:
                expression_choice = input("Enter the variable name to visualize its expression: ")
                if expression_choice in self.storage:
                    self.draw_parse_tree(str(self.storage[expression_choice]))
                else:
                    print("Invalid variable choice.")
                input("\n Press enter key to continue...")  

            elif num == 8:
                self.perform_matrix_vector_operations()
            elif num == 9:
                if self.safety:
                    state = 'Off'
                else:
                    state = 'On'
                choice = ''
                while choice not in ['y','n']:
                    choice = input(f'\n\nTurning this on will automatically convert assignment statements into the form of 1var = expression\nCurrent State:{state}\nDo you want to toggle auto simplification?(y/n): ')
                if choice == 'y':
                    self.safety = not self.safety
                    if self.safety:
                        print('Auto Simplification is now Off')
                    else:
                        print('Auto Simplification is now On')
                    input('\nPress enter key, to continue...')
                else:
                    pass
            elif num == 10:
                print('\nBye, thanks for using ST150/DSAA Assignment Statements Evaluation & Sorter')
                break
            else:
                print('Invalid Option! Please re-enter.')
    
    #Perform Matrix and Vector operations
    def perform_matrix_vector_operations(self):
        while True:
            operation_type = input("Do you want to perform Matrix or Vector Operations? [M/V]: ").upper()

            if operation_type not in ['M', 'V']:
                print("Invalid input. Please enter 'M' for Matrix or 'V' for Vector.")
                continue
            expression = input(f"Please enter {'Matrix' if operation_type == 'M' else 'Vector'} Expression: ")

            matrix_operation = MatrixOperation(expression)

            result = matrix_operation.perform_operation()

            if result is not None:
                print(f"Result: {result}")
            else:
                print("Unable to perform the operation. Please check your input.")

            another_expression = input("Evaluate another expression? [y/n]: ").lower()

            if another_expression != 'y':
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


    def SimultaneousEquation(self, var, statement, varlist):
        while True:
            equation2 = input(f'Simultaneous equation detected, please enter the second equation to complete a simultaneous equation (if you do not wish to continue with this, leave this input blank):\n')
            if equation2 == '':
                return
            try: 
                var2, statement2 = equation2.split('=' , 1)
                break
            except:
                print('Invalid input, please re-enter')
                continue
        #check if the variables in the 2 equations are the same
        varlist2 = re.findall(r'[a-zA-Z]+', equation2)
        varlist2 = list(set(varlist2))
        if varlist != varlist2:
            print('Cannot solve the simultaneous equations, The inputed variables are not the same')
            return
        #Move all variables to the left side of the equation
        var, statement = self.MoveVarLHS(var, statement)
        var2, statement2 = self.MoveVarLHS(var2, statement2)
        #store the 2nd equation into the storage
        tree = ParseTree(statement2)
        self.storage[var2] = tree
        #try to solve the equation using numpy
        import numpy as np
        #convert the equations into the "standard" Simultaneous equation form
        pattern = re.compile(r'[a-zA-Z]+')
        print(var, statement, var2, statement2)
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
        print(nparray, rhs)
        #solve the equations
        try:
            solution = np.linalg.solve(nparray, rhs)
            st = ''
            for i in range(len(solution)):
                st += f'{variables[i]} = {round(solution[i], 2)}\t'
            print(st)
            choice = ''
            while choice not in ['y','n']:
                choice = input('Do you want to save the solution?(y/n)\nNote that this will replace any assignments which may have the same name: ')
                if choice == 'y':
                    for i in range(len(solution)):
                        solution[i] = round(solution[i], 2)
                        self.storage[variables[i]] = ParseTree(f'{solution[i]}')
                else:
                    pass
        except:
            print('Cannot solve Simultaneous equations')
            pass
    
    def MoveVarLHS(self, var, statement):
        #Get all the variables on the right side of the equation
        match = re.findall(r'[a-zA-Z]+', statement)
        if len(match) == 0:
            return var, statement
        else:
            #Get all the variables on the right side of the equation
            match = re.findall('([+-]?\d*[a-z])', statement)
            #Move it to the left side of the equation
            tomove = match
            #Find all the numbers in the left side of the equation
            match = re.findall(r'([+-]?\d+)\b(?!\w)', var)
            #Move it to the right side of the equation
            tomove2 = match
            numbers = [int(num) for num in tomove2 if num]
            # Calculate the sum
            total_sum = sum(numbers)
            #Remove the numbers from the left
            var = re.sub(r'([+-]?\d+)\b(?!\w)', '', var)
            statement = ''
            if total_sum:
                if str(total_sum)[:1] == '-':
                    statement = f'{str(total_sum)[1:]}'
                else:
                    statement = f'-{total_sum}'
            #move the variable to the left side of the equation
            for i in tomove:
                if i[0] != '+' and i[0] != '-':
                    var += f'-{i}'
                elif i[0] == '-':
                    var += f'+{i[1:]}'
                else:
                    var += f'-{i[1:]}'
            return var, statement

            

            


    def draw_parse_tree(self, expression):
        parsed_tree = ParseTree(expression, self.storage)
        self._visualize_tree(parsed_tree.tree)

    def _visualize_tree(self, tree):
        try:
            screen = turtle.Screen()
            screen.title("Parse Tree Visualization")
            screen.setup(width=800, height=600)

            turtle.speed(0)  # Fastest
            turtle.up()  # move without drawing
            turtle.left(90)  # rot 90* to left
            turtle.backward(300)  # move back 300 units
            turtle.down()  # put pen down to start drawing

            self._draw_tree_recursive(tree, 300, 40)

            # Wait for the user to close the turtle graphics window
            turtle.exitonclick()

            # Close the current turtle graphics window
            turtle.bye()

            # Create a new turtle instance for the next drawing
            new_turtle = turtle.Turtle()

            # Reset the turtle state after creating the new turtle instance
            new_turtle.reset()

        except turtle.Terminator:
            pass

    def _draw_tree_recursive(self, tree, distance, angle, scale_factor=0.8):
        if tree is not None:
            turtle.forward(distance)
            turtle.write(str(tree.getKey()), align="center", font=("Arial", 12, "normal"))

            # Check if the key is a variable (contains only alphabetical characters)
            if isinstance(tree.getKey(), str) and tree.getKey().isalpha():
                # Branch out to the tree for the variable
                if tree.getKey() in self.storage:
                    # Draw the expression for the variable
                    turtle.left(angle)
                    turtle.penup()
                    turtle.forward(10)
                    turtle.pendown()
                    self._draw_tree_recursive(ParseTree(str(self.storage[tree.getKey()])).tree, distance * scale_factor*0.8, angle, scale_factor)
                    turtle.penup()
                    turtle.backward(10)
                    turtle.pendown()
                    turtle.right(angle)

                # Continue drawing the rest of the tree
                turtle.left(angle)
                self._draw_tree_recursive(tree.getLeftTree(), distance * scale_factor, angle, scale_factor)
                turtle.right(angle * 2)
                self._draw_tree_recursive(tree.getRightTree(), distance * scale_factor, -angle, scale_factor)
                turtle.left(angle)

            turtle.backward(distance)

            angle /= 2
            turtle.left(angle)
            self._draw_tree_recursive(tree.getLeftTree(), distance * scale_factor, angle, scale_factor)
            turtle.right(angle * 2)
            self._draw_tree_recursive(tree.getRightTree(), distance * scale_factor, -angle, scale_factor)
            turtle.left(angle)

if __name__ == '__main__':
    gui = Gui()
