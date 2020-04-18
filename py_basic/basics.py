#!/usr/bin/env python3
import platform
import os
import time

def isprime(n):
    if n <= 1:
        return False
    for x in range(2, n):
        if n % x == 0:
            return False
    else:
        return True

def fun_args(*args):
    if len(args):
        for s in args:
            print(s)
    else: print('Meow.')


def fibonacci(n):
    a, b = 0, 1
    while b < n:
        print(b, end = ' ', flush = True)
        a, b = b, a + b



def elapsed_time(f):
    def wrapper():
        t1 = time.time()
        f()
        t2 = time.time()
        print(f'Elapsed time: {(t2 - t1) * 1000} ms')
    return wrapper

@elapsed_time
def big_sum():
    num_list = []
    for num in (range(0, 100000)):
        num_list.append(num)
    print(f'Big sum: {sum(num_list)}')

def main():
    n = 5
    if isprime(n):
        print(f'{n} is prime')
    else:
        print(f'{n} not prime')

    fibonacci(1000)

    


    print('This is python version {}'.format(platform.python_version()))


    words = ['one', 'two', 'three', 'four', 'five']

    for i in words:
        print(i)

    n = 0
    while(n < 5):
        print(words[n])
        n += 1

    print(os.getcwd())

    x = 12
    y = 32

    if x < y:
        print('x < y: x is {} and y is {}'.format(x, y))

    x = 7
    print('x is {}'.format(x))
    print(type(x))

    print(os.path.abspath(__file__))
    print(os.path.dirname(os.path.abspath(__file__)))
    print(os.path.basename(os.path.abspath(__file__)))

    x = [ 1, 2, 3, 4, 5 ]
    for i in x:
        print('i is {}'.format(i))
        print(f'i is {i}')
        print("===")

    if True:
        print('if true')
    elif False:
        print('elif true')
    else:
        print('neither true')

    xx = True
    zz = 'xx' if xx else 'yy'
    print(zz)


    x = 0x0a
    y = 0x0c
    z = x & y
    print(f'(hex) x is {x:02x}, y is {y:02x}, z is {z:02x}')
    print(f'(bin) x is {x:08b}, y is {y:08b}, z is {z:08b}')

    fun_args('a','b','c')

    big_sum()
    

if __name__ == "__main__":
    main()
