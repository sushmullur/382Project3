# Authors: Ethan Yang and Sush Mullur
# Created 5/14/2022
import regex
import tabulate
#import pandas as pd
# 2d List for keeping track of truth table values.
table = [[]]

# List to keep track of all the variables within formula
variables = []

expression = "(implies (and p q r) (or p q r))"
#expression = "(implies (and p q r  (or s t)) (or (and  p q r s) (and p q r t)))"
#expression = "(and a (neg a))"


# main- currently used for testing
def main():
    temp =identify_variables(expression)
    temp = list(temp)
    vars =""
    print("List of variables: ")
    for i in temp:
        vars+=str(i)
        vars+=" "
    #print(vars)
    temp2 =output_table(temp)
    #print(temp2)
    temp3=check_tautology(temp2,expression)
    output = False
    Taut = True
    for i in range(len(temp3)):
        temp2[i]["output"]= temp3[i]
        if temp3[i]==True:
            output = True
        if temp3[i]==False:
            Taut = False
        #print(temp2[i])
    a="(implies p q)"
    tester(a)

    header = temp2[0].keys()
    rows = [x.values() for x in temp2]
    print(tabulate.tabulate(rows, header))

    #(tabulate(rows, header))
    if output:
        print("this statment is satisfiable")
    else:
        print("this statment is not satisfiable")
    if Taut:
        print("this statment is valid")
    else:
        print("this statment is not valid")


# Checks through the truth data iteratively and returns the validity of the statement.
# Complexity: O(n^2)

def convertImplies(input):
    if(input[0])=="implies":
        input[0]="or"
        if input[1][0]=="(":
            #input[1] = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[1][1:-1])]
            input[1]=convertImplies(helperSplitter(input[1][1:-1]))
        if input[1][0]=="(":
            #input[1] = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[1][1:-1])]
            input[1] = helperSplitter(input[1][1:-1])
        else:
            #input[1] = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[1])]
            input[1] = helperSplitter(input[1])
        input[1]= convertNeg(input[1])
        if input[2][0]=="(":
           # input[2] = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[2][1:-1])]
            #input[2]=convertImplies(input[2])
            input[2] = convertImplies(helperSplitter(input[2][1:-1]))
    return convertString(input)

def convertNeg(input):
    if input[0]=="neg":
        return input[1]
    if len(input[0])==1:
        return "(neg "+input[0]+")"
    elif input[0]=="and":
        input[0]="or"
    elif input[0]=="or":
        input[0]="and"
    elif input[0]=="iff":
        First = input[1]
        Second = input[2]
        notFirst = convertNeg(input[1])
        notSecond = convertNeg(input[2])
        return "(or (and"+First+" "+notSecond+")(and"+Second+" "+notFirst+"))"
    elif input[0]=="implies":
        return"(and ("+input[1]+") ("+convertNeg(input[2])+"))"
    for i in range(1, len(input)):
        if len(input[i])!=1:
            #input[i] = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[i][1:-1])]
            input[i]= helperSplitter(input[i][1:-1])
        input[i]=convertNeg(input[i])
    return convertString(input)
def convertString(input):
    ret = "("
    for curr in input:
        ret = ret + curr
        ret = ret + " "
    ret = ret[:-1]
    return ret + ")"
def tester(input):
    #input = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[1:-1])]
    input =helperSplitter(input[1:-1])
    count =0
    for curr in input:
        if curr[0]=="(":
            input[count]=tester(curr)
        count+=1
    if input[0] == "implies":
        input=convertImplies(input)
    elif input[0]=="neg" and len(input[1])!=1:
        #input = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[1][1:-1])]
        #input = helperSplitter(input[1][1:-1])
        input =convertNeg(helperSplitter(input[1][1:-1]))
    #for i in range(len(input)):
    else:
        return convertString(input)
    return input



def implies(input):
    if input[1]==True:
        return input[2] ==True
    return True
def iff(input):
    return input[1]==input[2]
def neg(input):
    if input[1]==True:
        return False
    return True
def andStatment(input):
    for i in input:
        if i == False:
            return False
    return True

def orStatment(input):
    for i in input:
        if i == True:
            return True
    return False
def helperSplitter(input):
    return [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input)]
def check_tautology(input, statement):
    def helper(input,statement):
        statement = helperSplitter((statement))
        count =0
        for curr in statement:
            if curr[0]=="(":
                statement[count] =helper(input, curr[1:-1])
            elif len(curr)==1:
                statement[count] = input[curr]
            count+=1
        if statement[0]=="and":
            return andStatment(statement)
        if statement[0]=="or":
            return orStatment(statement)
        if statement[0]=="implies":
            return implies(statement)
        if statement[0]=="iff":
            return iff(statement)
        if statement[0]=="neg":
            return neg(statement)
        else:
            return statement[0]
        ##put evreything together

        #return it

    ret = []
    for i in input:
        temp = statement
        ret.append(helper(i, temp))


    return ret


# Takes a formula as a string and places all the variables in the variables list
# O(n) complexity
def identify_variables(formula):
    # Creates a parsed list split by space
    space_removed = formula.split(" ")
    # Removes parentheses symbols to allow for easier variable identification
    for i in range(len(space_removed)):
        space_removed[i] = space_removed[i].replace("(", "")
        space_removed[i] = space_removed[i].replace(")", "")

    variables =  set()
    # Adds all identified and unique variables to the variables list
    for i in range(len(space_removed)):
        if len(space_removed[i]) == 1 and (space_removed[i] not in variables):
            variables.add(space_removed[i])
    print(variables)
    return variables


def output_table(input):
    input = list(input)
    ret = []
    curr = {}
    def helper(input, position, curr):
        if position >= len(input):
            ret.append(curr)
            return
        temp = curr.copy()
        temp2 = curr.copy()

        temp[input[position]] = True
        helper(input, position + 1, temp)

        temp2[input[position]] = False
        helper(input, position + 1, temp2)
        return

    helper(input, 0, curr)
    #print(ret)
    return ret


# valid tautologies for test cases
# (implies (and p q r) (or p q r))
# (iff (and p q r) (and p r q))
# implies (and p q r (or s t)) (or (and p q r s) (and p q r t)))


# get # of possible permutations and evaluate all of them. store within 2d list
# access all of those values and output it in the format of a truth table
# variable[i] = Header of table[i]

if __name__ == "__main__":
    main()
