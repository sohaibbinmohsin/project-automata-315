from yapl_lexer import *
from yapl_parser import *
import sys

global_env = (None, {})

def env_lookup(vname, env):
    if vname in env[1]:
        return env[1][vname]
    elif env[0] == None:
        return None
    else:
        return env_lookup(vname, env[0])

def env_update(vname, val, env):
    if vname in env[1]:
        env[1][vname] = val
    elif not (env[0] == None):
        env_update(vname, val, env[0])

def exp_eval(p, environment):
    operator = p[0]
    # print(operator)
    # if type(p[1]) == str:
    #     p[1] = var_val(p[1])
    # print('p1:',p[1])
    if operator == 'PAREN':
        return exp_eval(p[1], environment)
    elif operator == '+':
        return exp_eval(p[1], environment) + exp_eval(p[2], environment)
    elif operator == ',':
        # exp = [p[1], exp_eval(p[2])]
        return str(exp_eval(p[1], environment)) + " " + str(exp_eval(p[2], environment))
    elif operator == '-':
        return exp_eval(p[1], environment) - exp_eval(p[2], environment)
    elif operator == '*':
        return exp_eval(p[1], environment) * exp_eval(p[2], environment)
    elif operator == '/':
        return exp_eval(p[1], environment) / exp_eval(p[2], environment)
    elif operator == '%':
        return exp_eval(p[1], environment) % exp_eval(p[2], environment)
    elif operator == '^':
        return exp_eval(p[1], environment) ** exp_eval(p[2], environment)
    elif operator == 'INCREMENT':
        env_lookup(p[1], environment)[1] += 1
        return env_lookup(p[1], environment)[1]
    elif operator == 'DECREMENT':
        env_lookup(p[1], environment)[1] -= 1
        return env_lookup(p[1], environment)[1]
    elif operator == '<':
        return exp_eval(p[1], environment) < exp_eval(p[2], environment)
    elif operator == '>':
        return exp_eval(p[1], environment) > exp_eval(p[2], environment)
    elif operator == '<=':
        return exp_eval(p[1], environment) <= exp_eval(p[2], environment)
    elif operator == '>=':
        return exp_eval(p[1], environment) >= exp_eval(p[2], environment)
    elif operator == '==':
        return exp_eval(p[1], environment) == exp_eval(p[2], environment)
    elif operator == '!=':
        return exp_eval(p[1], environment) != exp_eval(p[2], environment)
    elif operator == '&&':
        return exp_eval(p[1], environment) and exp_eval(p[2], environment)
    elif operator == '||':
        return exp_eval(p[1], environment) or exp_eval(p[2], environment)
    elif operator == 'NOT':
        return not exp_eval(p[1], environment)
    elif operator == 'UMINUS':
        return (- exp_eval(p[1], environment))
    elif operator == 'POP':
        return env_lookup(p[1], environment)[1].pop(p[2])
    elif operator == 'PUSH':
        # print(environment[p[1]][1])
        return env_lookup(p[1], environment)[1].append(exp_eval(p[2], environment))
    elif operator == 'INDEX' or operator == 'ACCESS':
        return env_lookup(p[1], environment)[1][p[2]]
    elif operator == 'SLICE':
        x = slice(p[2], p[3])
        return env_lookup(p[1], environment)[1][x]
    elif operator == 'ASSIGN':
        # print('here')
        # print(environment[p[1]])
        env_lookup(p[1], environment)[1] = exp_eval(p[2], environment)
        return env_lookup(p[1], environment)[1]
    else:
        non_int = str(p[1])
        # non_int_ans = var_val(non_int)
        # if non_int_ans != '':
        #     return non_int_ans
        # print('p1:', p[1])
        if env_lookup(non_int, environment) == None:
            return p[1]
        else:
            return var_val(p[1], environment)
        
def assign_list(p, var, environment):
    operator = p[0]
    if operator == ",":
        assign_list(p[1], var, environment)
        assign_list(p[2], var, environment)
    else:
        env_lookup(var, environment)[1].append(p[1])
    
def var_check(p, environment):
    # print(p)
    # print(str(p[1]))
    var = str(p[1])
    # print('var:',var)
    # print(type(var))
    if env_lookup(var, environment) == None:
        # print(p[0])
        if p[0] == 'int':
            # print('hrr')
            # print(p[1])
            # print(type(p[1][1]))
            if type(p[1]) == int:
                # print('here')
                return True
            return False
        elif p[0] == 'float':
            if type(p[1]) == float:
                return True
            return False
        elif p[0] == 'char':
            v = p[1].strip("'")
            # print(v)
            # print(len(v))
            if len(v) == 1:
                return True
            return False
        elif p[0] == 'string':
            # print(type(p[1][1]))
            # v = p[1][1].strip('"')
            # if type(p[1][1]) == tuple:
            #     # print('here')
            #     return var_check(p[1][1])
            if type(p[1]) == str:
                return True
            return False
        elif p[0] == 'bool':
            if type(p[1]) == bool:
                return True
            return False
        else:
            return False
    else:
        # print(p[0])
        # print(environment[p[2]][0])
        var_type = env_lookup(var, environment)[0]
        if  var_type == p[0]:
            return True
        else:
            return False
        
def exp_assign(p, environment):
    # if p[1] != 'int' and p[1] != 'float' and p[1] != 'bool':
    # print('p2:', p[2])
    ans = exp_eval(p[2], environment)
    exp = (p[1], ans)
    # print('ans:', ans)
    if var_check(exp, environment) == False:
        raise TypeError('TypeError')
    if env_lookup(p[0], environment) != None:
        raise TypeError('RedeclerationError')
    if p[1] == 'char' and p[2][0] == 'CHAR':
        val = ans[1].strip("'")
        environment[1][p[0]] = [p[1], (ans[0], val)]
    else:
        environment[1][p[0]] = [p[1], ans]    
    
    
def var_val(p, environment):
    # print(p)
    ans = env_lookup(p, environment)
    # print(ans)
    val = ans[1]
    # print (val)
    # print(val in environment)
    if ans[0] == 'list':
        return val
    if env_lookup(val, environment) == None:
        # print('here')
        # print('val:', val)
        return val
    else:
        # print('here1')
        var_val(val, environment)
        
def stmt_eval(p, environment):
    # print(p)
    stype = p[0]
    # print(stype)
    local_env = (environment, {})
    if stype == 'PRINT':
        for i in range(1, len(p)):
            exp = p[i]
            # print('exp:', exp)
            # print(len(exp))
            # print(exp[1][0])
            # print(exp[1][1])
            if exp[1][0] == 'NAME':
                # if exp in environment:
                    
                # else:
                #     print(exp, end=' ')
                # print(exp[1][1])
                print(var_val(exp[1][1], environment), end=' ')
            else:
                print(exp_eval(exp, environment), end=' ')
        print(end='\n')
    elif stype == 'IF-ELSEIF-ELSE':
        # print('here')
        # print(exp_eval(p[1]))
        # print(p[2])
        # print(p[3][3][1])
        # print(exp_eval(p[3][1]))
        # print(p[5])
        if exp_eval(p[1], local_env) == True:
            run_program(p[2], local_env)
        elif exp_eval(p[3][1], local_env) == True:
            run_program(p[3][2], local_env)
        else:
            run_program(p[3][3][1], local_env)
    elif stype == 'DOWHILE':
        # print('local:',local_variables)
        # print(local_env)
        # print('here1')
        # print(environment)
        run_program(p[1], local_env)
        # print(environment)
        # local_variables['local'] = var
        # print('local:',local_variables)
        # print('var:',var)
        # print(exp_eval(p[2][1], var))
        while exp_eval(p[2][1], local_env) == True:
            # print('here')
            # print('local:',local_variables)
            run_program(p[1], local_env)
            # print(varr)
        environment[1].clear()
    elif stype == 'ASSIGN-LIST':
        # print(p[1])
        # print(p[2])
        # print(exp_eval(p[2]).split(" "))
        # print(len(p[2]))
        # environment[p[1]] = exp_eval(p[2]).split(" ")
        environment[1][p[1]] = ('list', [])
        assign_list(p[2], p[1], environment)
        # print(environment)
    elif stype == 'ASSIGN-EMPTY-LIST':
        environment[1][p[1]] = ('list', [])
        # print(environment)
    elif stype == 'POP' or stype == 'PUSH' or stype == 'INDEX' or stype == 'SLICE' or stype == 'ACCESS' or stype == 'ASSIGN':
        # environment[p[1]].pop(p[2])
        exp_eval(p, environment)
        # print(environment)
    elif stype == 'INCREMENT' or stype == 'DECREMENT':
        exp_eval(p, environment)
    elif stype == 'CALL':
        val = env_lookup(p[1], environment)
        if(val[0] == 'function'):
            param = val[1]
            body = val[2]
            env = val[3]
            if len(p[2]) != len(param):
                print("wrong no of args")
            else:
                new_env = (env, {})
                for i in range(0, len(p[2])):
                    arg_val = exp_eval(p[2][i], environment)
                    new_env[1][param[i]] = arg_val
                try:
                    run_program(body, new_env)
                    return None
                except Exception as return_value:
                    return return_value
        else:
            print("call to non-function")
    else:
        exp_assign(p, environment)
        # print('here2')
        # print(environment)

def run_program(p, environment):
    for stmt in p:
        # print ("stmt:", stmt)
        if stmt != None:
            # print('here4')
            # print(environment)
            # print(stmt)
            stmt_eval(stmt, environment)
            # print('here3')
            # print(environment)
            
if len(sys.argv) == 1:
    print('File name/path not provided as cmd arg.')
    exit(1)

while True:
    fileHandler = open(sys.argv[1], "r")
    userIn = fileHandler.read()
    fileHandler.close()
    
    print("Welcome to your YAPL's Interpreter")
    parsed = parser.parse(userIn)
    if not parsed:
        continue
    
    for line in userIn.split('\n'):
        print(line)
        
    print('==========================================\n{OUTPUT}')
    try:
        run_program(parsed, global_env)
    except Exception as e:
        print(e)
        
    input("Press any key to run code again")
    
exit()