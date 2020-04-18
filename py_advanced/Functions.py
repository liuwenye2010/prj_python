# Demonstrate the use of keyword-only arguments
# Demonstrate the use of function docstrings
# Use lambdas as in-place functions
# Demonstrate the use of variable argument lists

# define a function that takes variable arguments
def addition(base, *args):
    result = 0
    for arg in args:
        result += arg
    return result

def CelsisusToFahrenheit(temp):
    return (temp * 9/5) + 32


def FahrenheitToCelsisus(temp):
    return (temp-32) * 5/9


def myFunctiondocstrings(arg1, arg2=None):
    """myFunctiondocstrings(arg1, arg2=None) 

    Parameters:
    arg1: the first argument. 
    arg2: the second argument. Defaults to None. 
    """
    print(arg1, arg2)

# use keyword-only arguments to help ensure code clarity
def myFunction(arg1, arg2, *, suppressExceptions=False):
    print(arg1, arg2, suppressExceptions)


def main():
    # try to call the function without the keyword
    print(myFunctiondocstrings.__doc__)
    # myFunction(1, 2, True)
    myFunction(1, 2, suppressExceptions=True)

    ctemps = [0, 12, 34, 100]
    ftemps = [32, 65, 100, 212]

    # Use regular functions to convert temps
    print(list(map(FahrenheitToCelsisus, ftemps)))
    print(list(map(CelsisusToFahrenheit, ctemps)))

    # Use lambdas to accomplish the same thing
    print(list(map(lambda t: (t-32) * 5/9, ftemps)))
    print(list(map(lambda t: (t * 9/5) + 32, ctemps)))

    # pass different arguments
    print(addition(5, 10, 15, 20))
    print(addition(1, 2, 3))

    # pass an existing list
    myNums = [5, 10, 15, 20]
    print(addition(*myNums))

if __name__ == "__main__":
    main()
