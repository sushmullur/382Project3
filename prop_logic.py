# Authors: Ethan Yang and Sush Mullur
# Created 5/14/2022

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
    output_table(temp)


# Checks through the truth data iteratively and returns the validity of the statement.
# Complexity: O(n^2)
def check_tautology():
    for i in range(len(table)):
        for j in range(len(table[i])):
            if not table[i][j]:
                return False
    return True


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
