# Authors: Ethan Yang and Sush Mullur
# Created 5/14/2022
# Last modified 5/27/2022
import regex
import tabulate


# Main method. All the methods for the 3 questions are run here.
def main():
    # Expression is read from the file.
    expression = file_read("test.txt")
    print_table(expression)
    a = expression
    print("CNF form is: ",CNFConverter(a))
    temp =a
    a= CNFConverter(a)
    resoloution(a)

#(and (and (or (neg p) q) (or (neg q) p)) (or (or p q) (or (neg p) (neg q))))
# This functions reads a file line by line and returns a given expression.
# This function ignores comments in the test file.
def file_read(filename):
    file = open(filename, "r")
    ret_val = ""
    for line in file.readlines():
        if line[0] != '#':
            ret_val += line
    return ret_val.strip()


# --------------------------------------------------------------------------------------------------------------------
# Question 1
# Outputs the table for question 1. Also determines if the statement is satisfiable and/or valid.
def print_table(input):
    temp = identify_variables(input)
    temp = list(temp)
    vars = ""
    for i in temp:
        vars += str(i)
        vars += " "
    table = output_to_dict(temp)
    results = check_tautology(table, input)
    output = False
    Taut = True

    for i in range(len(results)):
        table[i]["output"] = results[i]
        if results[i] == True:
            output = True
        if results[i] == False:
            Taut = False

    # Tabulate is used to format the truth table.
    header = table[0].keys()
    rows = [x.values() for x in table]
    print(tabulate.tabulate(rows, header))
    if output:
        print("this statement is satisfiable")
    else:
        print("this statement is not satisfiable")
    if Taut:
        print("this statement is valid")
    else:
        print("this statement is not valid")


# This function handles the case of implies between two values.
def implies(input):
    if input[1] == True:
        return input[2] == True
    return True


# This function handles the case of if and only if between two values.
def iff(input):
    return input[1] == input[2]


# This function handles negation of a value.
def neg(input):
    if input[1] == True:
        return False
    return True


# This function handles and between values.
def andStatment(input):
    for i in input:
        if i == False:
            return False
    return True


# This function handles or between values.
def orStatment(input):
    for i in input:
        if i == True:
            return True
    return False


# This helper function splits up an expression using the regex library.
def helperSplitter(input):
    return [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input)]


# This function performs the initial steps and calculations for checking tautology.
def check_tautology(input, statement):
    def helper(input, statement):
        statement = helperSplitter((statement))
        count = 0
        for curr in statement:
            if curr[0] == "(":
                statement[count] = helper(input, curr[1:-1])
            elif len(curr) == 1:
                statement[count] = input[curr]
            count += 1

        # Different cases and statements are handled.
        if statement[0] == "and":
            return andStatment(statement)
        if statement[0] == "or":
            return orStatment(statement)
        if statement[0] == "implies":
            return implies(statement)
        if statement[0] == "iff":
            return iff(statement)
        if statement[0] == "neg":
            return neg(statement)
        else:
            return statement[0]

    ret = []
    for i in input:
        temp = statement
        ret.append(helper(i, temp))
    return ret


# Takes a formula as a string and places all the variables in the variables list
def identify_variables(formula):
    # Creates a parsed list split by space
    space_removed = formula.split(" ")
    # Removes parentheses symbols to allow for easier variable identification
    for i in range(len(space_removed)):
        space_removed[i] = space_removed[i].replace("(", "")
        space_removed[i] = space_removed[i].replace(")", "")

    variables = set()
    # Adds all identified and unique variables to the variables list
    for i in range(len(space_removed)):
        if len(space_removed[i]) == 1 and (space_removed[i] not in variables):
            variables.add(space_removed[i])
    print(variables)
    return variables


# Outputs the truth table into a dictionary to create a 2d representation.
def output_to_dict(input):
    input = list(input)
    input.sort()
    ret = []
    curr = {}
    # Helper method for recursion.
    def helper(input, position, curr):
        # Base case
        if position >= len(input):
            ret.append(curr)
            return
        branch = curr.copy()
        branch2 = curr.copy()
        branch[input[position]] = True
        helper(input, position + 1, branch)
        branch2[input[position]] = False
        helper(input, position + 1, branch2)
        return

    helper(input, 0, curr)
    return ret


# --------------------------------------------------------------------------------------------------------------------
# Question 2

# Converts implies statements to CNF form.
def convertImplies(input):
    if (input[0]) == "implies":
        input[0] = "or"
        if input[1][0] == "(":
            input[1] = convertImplies(helperSplitter(input[1][1:-1]))
        if input[1][0] == "(":
            input[1] = helperSplitter(input[1][1:-1])
        else:
            input[1] = helperSplitter(input[1])
        input[1] = convertNeg(input[1])
        if input[2][0] == "(":
            input[2] = convertImplies(  helperSplitter(input[2][1:-1]))
    return convertString(input)


# Converts iff statements to CNF form.
def convertIff(input):
    first = input[1]
    second = input[2]
    if input[1][0] == "(":
        input[1] = helperSplitter(input[1][1:-1])
    else:
        input[1] = helperSplitter(input[1])
    if input[2][0] == "(":
        input[2] = helperSplitter(input[2][1:-1])
    else:
        input[2] = helperSplitter(input[2])
    notFirst = convertNeg(input[1])
    notSecond = convertNeg(input[2])
    return "(and (or " + first + " " + notSecond + ") (or " + second + " " + notFirst + "))"


# Handles converting not statements and expressions to CNF form.
def convertNeg(input):
    if input[0] == "neg":
        return input[1]
    if len(input[0]) == 1:
        return "(neg " + input[0] + ")"
    elif input[0] == "and":
        input[0] = "or"
    elif input[0] == "or":
        input[0] = "and"

    for i in range(1, len(input)):
        if len(input[i]) != 1:
            input[i] = helperSplitter(input[i][1:-1])
        input[i] = convertNeg(input[i])
    return convertString(input)


# This function is used in converting the list to a string that can be output.
def convertString(input):
    ret = "("
    for curr in input:
        ret = ret + curr
        ret = ret + " "
    ret = ret[:-1]
    return ret + ")"

def CNFConverter(input):
    ret = convertToCNF(input)
    temp, ret = noNest(ret, "abc")
    ret = convertString(ret)
    ret = distribute(ret)
    temp, ret = noNest(ret, "abc")
    ret = convertString(ret)
    return ret
def CNFConverterNest(input):
    ret = convertToCNF(input)
    ret = distribute(ret)
    return ret

# Converts a given input to CNF
def convertToCNF(input):
    # input = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[1:-1])]
    input = helperSplitter(input[1:-1])
    count = 0
    for curr in input:
        if curr[0] == "(":
            input[count] = convertToCNF(curr)
        count += 1
    if input[0] == "implies":
        input = convertImplies(input)
    elif input[0] == "iff":
        input = convertIff(input)
    elif input[0] == "neg" and len(input[1]) != 1:
        # input = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[1][1:-1])]
        # input = helperSplitter(input[1][1:-1])
        input = convertNeg(helperSplitter(input[1][1:-1]))
    # for i in range(len(input)):
    else:
        ret = convertString(input)
        #ret = distribute(ret)
        return ret
    return input

#handles distributive laws for the CNF form(kinda ugly somtimes)
def distribute(input):
    if input[0]=="(":
        input = input[1:-1]
    input = helperSplitter(input)
    if input[0]=="and":
        return convertString(input)
    andLine = -1
    count =0
    for item in input:
        if count == 0:
            count+=1
            continue
        if item[0:4] == "(and":
            andLine = count
            break
        count+=1
    if (andLine >0):
        divClause = input[andLine]
        temp = []
        temp.append("and")
        divClause=divClause[5:-1]
        divClause=helperSplitter(divClause)

        for item in divClause:
            a = input
            a[andLine] = item
            a=convertString(a)
            temp.append(a)
        ret = ["and"]
        count =0
        for item in temp:
            if count == 0:
                count+=1
                continue
            #return distribute(item)
            ret.append(distribute(item))
            count+=1

        return convertString(ret)

    else:
        # there is no "AND", can't move "OR" inside further
        return convertString(input)
#gets rid of nested ors and ands
def noNest(input, sign):
    input = helperSplitter(input[1:-1])
    if input[0] == "neg":
        return False, (input)
    tempS = input[0]
    count = 0
    while count< len(input):
        if input[count][0] == "(":
            result, temp = noNest(input[count], tempS)
            if result:
                input.remove(input[count])
                input+=temp
                count-=1
            else:
                input[count]=convertString(temp)
        count+=1
    if tempS==sign:
        return True, input[1:]
    else:
        return False, input

#helper for question 1
def helper(input, distributed):
    ret =[]
    if input[0]=="(":
        input = helperSplitter(input[1:-1])
        if input[0]=="and":
            return None
        if input[0]!="neg":
            input = input[1:]
        else:
            temp= convertString(input)
            temp2 = []
            temp2.append(temp)
            input=temp2
    for i in input:
        for i2 in distributed:
            ret.append("(or "+i+" "+i2+")")

    return ret


# --------------------------------------------------------------------------------------------------------------------
# Question 3

#helper for converting negation for quesiton 3(not used anymore)
def convertNegRes(input):
    if input[0] == "neg":
        return input[1]
    if len(input[0]) == 1:
        return ["neg", input[0]]

#negation for propositional statments
def convertNegProp(input):
    if input[0]=="(":
        input = helperSplitter(input[1:-1])
    else:
        input = helperSplitter(input)
    if len(input)==1:
        return"(neg "+input[0]+")"
    if input[0] == "implies":
        input[0] = "and"
        input[1]= convertNegProp(input[1])
    elif input[0] == "iff":
        input ="(or (and" + input[1] + " " + convertNegProp(input[2]) + ")(and" + input[2] + " " + convertNegProp(input[1]) + "))"
        return input
    elif input[0] == "neg":
        input = input[1]
    elif input[0]=="and":
        count =0
        for i in input:
            if i=="and":
                input[count]="or"
            else:
                input[count]= convertNegProp(i)
            count+=1
    elif input[0]=="or":
        count =0
        for i in input:
            if i=="or":
                input[count]="and"
            else:
                input[count]= convertNegProp(i)
            count+=1
    # for i in range(len(input)):
    if len(input)>1:
        return convertString(input)
    return input

def resoloution(input):
    input =input[1:-1]
    input =helperSplitter(input)
    if input[0]=="or":
        input = help_cancel(convertString(input))
        if input==None:
            print ("can resolve")
            return
        print("can't resolve")
        return
    input = input[1:]
    ret = input
    count =0

    check =["a"]
    count =0
    for i in input:
        i=help_cancel(i)
        if i !=None:
            if i[0]=="(":
                check = helperSplitter(i[1:-1])
                check = check[1:]

            for i2 in input:
                if i ==i2:
                    pass
                else:
                   check =helperCheck(check, i2)
            if check !=[]:
                print("cant resolve")
                return
    print("can resolve")
    return
#checks to clauses to see if they have similar items
def helperCheck(input1, input2):
    ret =[]
    if input2[0]=="(":
        input2=helperSplitter(input2[1:-1])
        input2=input2[1:]
    for i in input1:
        flag = True
        for i2 in input2:
            if i == convertNegProp(i2):
                flag = False
        if flag:
            ret.append(i)
    return ret


#checks if anything in or statments cancels out
def help_cancel(input):
    if len(input)==1:
        return input
    ret = helperSplitter(input[1:-1])
    temp = helperSplitter(input[1:-1])
    if temp[0]=="and":
        return input
    input = helperSplitter(input[1:-1])
    ret = ret[1:]

    for i in input:
        negated = convertNegProp(i)
        for i2 in temp:
            if negated ==i2:
                if i2 in ret:
                    ret.remove(i2)
                    hasChanged=True
                if i in ret:
                    ret.remove(i)
                    hasChanged=True
                return None  ##BIG CHANGE
    if len(ret)==0:
        return None
    else:
        return convertString(ret)
    

"""
def help_cancel(input):

    input2 = convertNegProp(input)
    input2 = convertToCNF(input2)
    #input = convertAnd(input)
    input = convertToCNF(input)
    temp =getVar(input)
    temp2 = getVar(input2)
    res =[]
    res2 =[]
    i =0

    while i < len(temp):
        if len(temp[i])==1:
            res.append(temp[i])
        elif temp[i]== "neg" or temp[i]=="not":
            negation =["neg",temp[i+1]]
            #negation = "neg "+temp[i+1]
            res.append(negation)
            i=i+1
        i = i + 1
    i =0


    while i < len(temp2):
        if len(temp2[i]) == 1:
            res2.append(temp2[i])
        elif temp2[i] == "neg" or temp2[i] == "not":
            negation = ["neg", temp2[i + 1]]
            # negation = "neg "+temp[i+1]
            res2.append(negation)
            i = i + 1
        i = i + 1

    terms = res2.copy()
    for i in res2:
        negated = convertNegRes(i)
        for i2 in res:
            if i2 ==negated:
                if i in terms:
                    terms.remove(i)
                break

    if len(terms)==0:
        #print("Resolution ended with all elements gone")
        return None
    else:
        #print("terms still left after resolotion")
        ret="or"+terms
        return convertString(ret)
"""
def getVar(input):
    input = input.replace('(','').replace(')','')
    return input.split()

def distributivity(expression):
    # (and (or p q) (or r s)) input
    # expect (or (and p r) (and p s) (and q r) (and q s)
    # isolate "binomials"
    # multiply them
    help_distribute(expression)
    # temp = helperSplitter(expression[1:-1])
    # print(temp)


def help_distribute(expression):
    if expression[0] == '(':
        expression = expression[1:-1]
    expression = helperSplitter(expression)
    and_index = 9999999
    for i in range(len(expression)):
        if expression[i] == "and":
            and_index = i
            if expression[i] == "or" and and_index < i:
            # perform distribution
                pass



if __name__ == "__main__":
    main()
    distributivity("(and (or p q) (or r s))")
