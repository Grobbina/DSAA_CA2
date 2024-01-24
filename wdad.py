import re   

def checkstat(var, statement):
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
            
var, statement = checkstat('2x','16+3x+y+4y+2x')
print(var)
print(statement)
                        