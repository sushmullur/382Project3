# Authors: Ethan Yang and Sush Mullur
# Created 5/14/2022

# 2d List for keeping track of truth table values.
table = [[]]

# List to keep track of all the variables within formula
variables = []

expression = "(implies (and p q r) (or p q r))"


# main- currently used for testing
def main():
    identify_variables(expression)
    print("List of variables: " + str(variables))
    output_table()


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

    global variables
    # Adds all identified and unique variables to the variables list
    for i in range(len(space_removed)):
        if len(space_removed[i]) == 1 and (space_removed[i] not in variables):
            variables.append(space_removed[i])


def output_table():
    table_string = "Truth Table:\n"
    for variable in variables:
        table_string += variable + "\t"

    table_string += expression
    # TODO: Print out all T and F permutations
    print(table_string)


# valid tautologies for test cases
# (implies (and p q r) (or p q r))
# (iff (and p q r) (and p r q))
# implies (and p q r (or s t)) (or (and p q r s) (and p q r t)))


# get # of possible permutations and evaluate all of them. store within 2d list
# access all of those values and output it in the format of a truth table
# variable[i] = Header of table[i]

if __name__ == "__main__":
    main()
