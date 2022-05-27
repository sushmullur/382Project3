# Authors: Ethan Yang and Sush Mullur
# Created 5/14/2022
import regex
import tabulate



# expression = "(implies (and p q r  (or s t)) (or (and  p q r s) (and p q r t)))"
# expression = "(and a (neg a))"


# main- currently used for testing
def main():
    expression = file_read("test.txt")
    finalOutput(expression)
    a = expression
    print(convertToCNF(a))
    Resoloution(a)

def file_read(filename):
    file = open(filename, "r")
    return file.read()

# --------------------------------------------------------------------------------------------------------------------
# Question 1
def finalOutput(input):
    temp = identify_variables(input)
    temp = list(temp)
    vars = ""
    for i in temp:
        vars += str(i)
        vars += " "
    table = output_table(temp)
    results = check_tautology(table, input)
    output = False
    Taut = True

    for i in range(len(results)):
        table[i]["output"] = results[i]
        if results[i] == True:
            output = True
        if results[i] == False:
            Taut = False

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

def implies(input):
    if input[1] == True:
        return input[2] == True
    return True


def iff(input):
    return input[1] == input[2]


def neg(input):
    if input[1] == True:
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
    def helper(input, statement):
        statement = helperSplitter((statement))
        count = 0
        for curr in statement:
            if curr[0] == "(":
                statement[count] = helper(input, curr[1:-1])
            elif len(curr) == 1:
                statement[count] = input[curr]
            count += 1
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
# O(n) complexity
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


def output_table(input):
    input = list(input)
    ret = []
    curr = {}

    def helper(input, position, curr):
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
    # print(ret)
    return ret


# --------------------------------------------------------------------------------------------------------------------
# Question 2

def convertImplies(input):
    if (input[0]) == "implies":
        input[0] = "or"
        if input[1][0] == "(":
            # input[1] = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[1][1:-1])]
            input[1] = convertImplies(helperSplitter(input[1][1:-1]))
        if input[1][0] == "(":
            # input[1] = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[1][1:-1])]
            input[1] = helperSplitter(input[1][1:-1])
        else:
            # input[1] = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[1])]
            input[1] = helperSplitter(input[1])
        input[1] = convertNeg(input[1])
        if input[2][0] == "(":
            # input[2] = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[2][1:-1])]
            # input[2]=convertImplies(input[2])
            input[2] = convertImplies(helperSplitter(input[2][1:-1]))
    return convertString(input)


def convertIff(input):
    # p iff q becomes  (and (or (neg p) q) (or p (neg q)))
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



def convertNeg(input):
    if input[0] == "neg":
        return input[1]
    if len(input[0]) == 1:
        return "(neg " + input[0] + ")"
    elif input[0] == "and":
        input[0] = "or"
    elif input[0] == "or":
        input[0] = "and"

    # elif input[0] == "iff":
    #    First = input[1]
    #    Second = input[2]
    #    notFirst = convertNeg(input[1])
    #    notSecond = convertNeg(input[2])
    #    return "(or (and" + First + " " + notSecond + ")(and" + Second + " " + notFirst + "))"
    # elif input[0] == "implies":
    #    return "(and (" + input[1] + ") (" + convertNeg(input[2]) + "))"
    for i in range(1, len(input)):
        if len(input[i]) != 1:
            # input[i] = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", input[i][1:-1])]
            input[i] = helperSplitter(input[i][1:-1])
        input[i] = convertNeg(input[i])
    return convertString(input)


def convertString(input):
    ret = "("
    for curr in input:
        ret = ret + curr
        ret = ret + " "
    ret = ret[:-1]
    return ret + ")"


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
        return convertString(input)
    return input
# --------------------------------------------------------------------------------------------------------------------
# Question 3
def convertNegRes(input):
    if input[0] == "neg":
        return input[1]
    if len(input[0]) == 1:
        return ["neg", input[0]]
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


def Resoloution(input):
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
        print("resoloution eneded with all elements gone")
    else:
        print("terms still left after resolotion")
def getVar(input):
    input = input.replace('(','').replace(')','')
    return input.split();

if __name__ == "__main__":
    main()
