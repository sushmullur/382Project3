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
    a = "(iff (and (neg p) q) r)"
    print(convertToCNF(a))

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
    temp2 = output_table(temp)
    temp3 = check_tautology(temp2, input)
    output = False
    Taut = True
    for i in range(len(temp3)):
        temp2[i]["output"] = temp3[i]
        if temp3[i] == True:
            output = True
        if temp3[i] == False:
            Taut = False
    header = temp2[0].keys()
    rows = [x.values() for x in temp2]
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
        temp = curr.copy()
        temp2 = curr.copy()

        temp[input[position]] = True
        helper(input, position + 1, temp)

        temp2[input[position]] = False
        helper(input, position + 1, temp2)
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

if __name__ == "__main__":
    main()
