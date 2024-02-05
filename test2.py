import re

def MoveVarLHS(var, statement):
        #find all "words" in the var side of the equation (variables)
        match = re.findall(r'[a-zA-Z]+', var)
        #if there is only 1 variable in the var side of the equation
        if len(match) == 1:
            return var, statement
        else:
            for i in range(len(match)-1):
                match = re.search('([+-]?\d*)[0-9]*[a-zA-Z]+', var)
                tokeep = match.group()
                tomove = var.replace(tokeep, '')
                #check if the variables are already in the storage, if it is, we use another variable to store the equation, 
                #if all variables are, replace the last variable in storage with the equation
                for i in range(len(match)-1):
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
            

if __name__ == '__main__':
    print(MoveVarLHS(var = '3x+2y+3z', statement = '0')) # ('3x', '-3y-3z')
    print(MoveVarLHS(var = '3x+2y+3z', statement = '3x+2y+3z')) # ('3x', '0')
