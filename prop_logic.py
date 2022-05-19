# Authors: Ethan Yang and Sush Mullur
# Created 5/14/2022
import regex
# 2d List for keeping track of truth table values.
table = [[]]

# List to keep track of all the variables within formula
variables = []

expression = "(implies (and p q r) (or p q r))"


# main- currently used for testing
def main():
    temp =identify_variables(expression)
    print("List of variables: ")
    for i in temp:
        print(i," ")
    temp2 =output_table(temp)
    check_tautology(temp2,expression)


# Checks through the truth data iteratively and returns the validity of the statement.
# Complexity: O(n^2)
def implies(input):
    return input[0]==input[1]
def iff(input):
    prev = -1
    for i in range(len(input)):
        if input[i] == True or input[i]==False:
            if prev!=-1:
                if input[i]!=input[prev]:
                    return False
                prev +=1
            else:
                prev = i
    return True
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
def check_tautology(input, statment):
    def helper(input,statement):
        statement = [match.group() for match in regex.finditer(r"(?:(\((?>[^()]+|(?1))*\))|\S)+", statement)]
        for curr in statment:
            if curr[0]=="(":
                curr =helper(input, curr)
            elif len(curr)==1:
                curr = input[curr]
        if statement[0]=="and":
            return andStatment(statment)
        if statment[0]=="or":
            return orStatment(statment)
        if statment[0]=="implies":
            return implies(statment)
        if statment[0]=="iff":
            return iff(statment)
        ##put evreything together

        #return it

    ret = False
    for i in input:
        temp = statment.copy()
        helper(i, temp)


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
    print(ret)
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
