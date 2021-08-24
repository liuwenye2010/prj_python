#!/usr/bin/python
"""A one line summary of the module or program, terminated by a period.
"""
import os
#autopep8/ yapf / pep8 /pylint /
#> yapf --style google -i test.py
#> autopep8  -i test.py

names = ['ads', 'hps', 'johl']

# TODO(johl@synaptics.com): Use a "*" here for string repetition.
x = ("hdddddd" "hhhh")


def print_xyz(x, y, z):
    print(f"x:{x}")
    print(f"y:{y}")
    print(f"z:{z}")


class BoundRepeater:
    """ Iterator
    """

    def __init__(self, value, max):
        self.value = value
        self.max = max
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count > self.max:
            raise StopIteration
        self.count = self.count + 1
        return self.value


def boundrepeat(value, max):
    """ Generator
    """
    count = 0
    while True:
        if count >= max:
            return
        count = count + 1
        yield value


def squired(values):
    for i in values:
        yield i**2


def negated(values):
    for i in values:
        yield -i


def add_a(x, y):
    return x + y


#dirtion to simulate the C switch
def dispatch_if(operator, x, y):
    return {
        'add': lambda x,y : x + y, #add_a(x, y),
        'sub': lambda x,y : x - y,
        'add_a': add_a,
    }.get(operator, lambda: None)(x,y)


if __name__ == "__main__":
    assert (1 == 2, "this should fail")
    print(x)
    xyz = [1, 2, 3]
    print_xyz(*xyz)
    xyz_gen = (x for x in range(1, 4))
    print_xyz(*xyz_gen)
    {x: x**2 for x in range(10) if x % 2 == 0}
    print(xyz[::-1])
    xyz.reverse()
    print(xyz)
    print([i for i in reversed(xyz)])
    brept = BoundRepeater('HI', 10)
    for item in brept:
        print(item)
    print("====")
    for item in brept:  # iterator had done,nothing output
        print(item)
    print("====")

    #generator is one function
    for item in boundrepeat('HELLO', 10):
        print(item)
    print("====")

    #generator expression
    boundrepeat_iter = ("HELLO" for i in range(10))
    for i in boundrepeat_iter:
        print(i)

    boundrepeat_iter = (i for i in range(10))
    chain = negated(squired((boundrepeat_iter)))
    print(list(chain))
    print("====")
    squred_iter = (x * x for x in range(10))
    negated_iter = (-x for x in squred_iter)
    print(list(negated_iter))
    print(dispatch_if('add', 1, 2))
    print(dispatch_if('sub', 1, 2))
    print(dispatch_if('add_a', 1, 2))


    print("done")
    pass
