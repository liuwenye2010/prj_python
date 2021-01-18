#!usr/bin/env python
#howto-functional.pdfs
import pprint 
import os 
import random
import itertools #排列permutation组合combinations， 分组groupby 最有用
import functools #高阶函数接受一个或多个函数作为输入，返回新的函数。这个模块中最有用的工具是 functools.partial() 函数
import operator

def demo_functional_prg():
    m = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    for key in m:
        print(key, m[key])

    S = {2, 3, 5, 7, 11, 13}
    for i in S:
        print(i)

    line_list = [' line 1\n', 'line 2 \n']
    # Generator expression -- returns iterator
    stripped_iter = (line.strip() for line in line_list)
    # List comprehension -- returns list
    stripped_list = [line.strip() for line in line_list]
    #choose the sepecial lines 
    stripped_list = [line.strip() for line in line_list if line != ""]
    ##
    seq1 = 'abc'
    seq2 = (1, 2, 3)
    xy = [(x, y) for x in seq1 for y in seq2] #doctest: +NORMALIZE_WHITESPACE
    print(xy)
    pprint.pprint(xy)
# [('a', 1), ('a', 2), ('a', 3),
# ('b', 1), ('b', 2), ('b', 3),
# ('c', 1), ('c', 2), ('c', 3)]

   #generator 
def generate_ints(N):
    for i in range(N):
        yield i
# A recursive generator that generates Tree leaves in in-order.
def inorder(t):
    if t:
        for x in inorder(t.left):
            yield x
        yield t.label
        for x in inorder(t.right):
            yield x


def upper(s):
    return s.upper()

def xfun(x):
    return(x**2 + x)

def is_even(x):
    return (x % 2) == 0

def get_state(city_state):
    return city_state[1]

def log(message, subsystem):
    """Write the contents of 'message' to the specified subsystem."""
    print('%s: %s' % (subsystem, message))

if __name__ == "__main__":
    demo_functional_prg()
    gen = generate_ints(3)
    for i in gen:
        print(i)
#map and filter 
    list_map = list(map(upper, ['sentence', 'fragment']))
    print(list_map)
    list_map = [upper(s) for s in ['sentence', 'fragment']]
    print(list_map)
    x = [1,2,3,5,6]
    y = [xfun(i) for i in x]
    print(y)
    #
    #list(filter(is_even, range(10))
    for item in enumerate(['subject', 'verb', 'object']):
        print(item)
    pass

    #enumerate() 常常用于遍历列表并记录达到特定条件时的下标:
    #>>> below can not work ?
    f = open('dummy.txt', 'rt')
    for i, line in enumerate(f):
        if line.strip() == '':
            print('Blank line at line #%i' % i)
    #<<<
    # Generate 8 random numbers between [0, 10000)
    rand_list = random.sample(range(10000), 8)
    print(rand_list)
    ls1 = sorted(rand_list)
    print(ls1)
    ls2 = sorted(rand_list,reverse=True)
    print(ls2)
    print(any([0, 1, 0]))
    print(all([0, 1, 0]))
    #zip(iterA, iterB, ...) 从每个可迭代对象中选取单个元素组成列表并返回:
    print(zip(['a', 'b', 'c'], (1, 2, 3)))
    
    #Itertools 
    #itertools.count(10)
    #排列组合之组合
    itx = itertools.combinations([1, 2, 3, 4, 5], 2) # C52 = 5*4 /2*1 = 10
    for i, x in enumerate(itx):
        print(i,x)
    #排列组合之排列
    itx = itertools.permutations([1, 2, 3, 4, 5], 3) # A53 = 5*4*3 = 60
    for i, x in enumerate(itx):
        print(i,x)
    
    #gproup by   
    #itertools.groupby(iter,key_func=None)
    #key_func(elem)
    city_list = [('Decatur', 'AL'), ('Huntsville', 'AL'), ('Selma', 'AL'),
('Anchorage', 'AK'), ('Nome', 'AK'),
('Flagstaff', 'AZ'), ('Phoenix', 'AZ'), ('Tucson', 'AZ')]

    itg = itertools.groupby(city_list, key = get_state) # 返回一个长度为 2 的元组的数据流, 每个元组包含键值以及对应这个键值的元素所组成的迭代器。
    for key,items in itg:
        print("key:%s"%key)
        for item in items:
            print(item)
        

    #functools 
    server_log = functools.partial(log, subsystem='server')
    server_log('Unable to open socket')
    #
    y = functools.reduce(operator.concat, ['A', 'BB', 'C'])
    print(y)
    y = functools.reduce(operator.mul, [1, 2, 3], 1) #连续乘法
    print(y)
    
    y = itertools.accumulate([1, 2, 3, 4, 5])
    for x in y:
        print(x,end =" ")
    #不过, 对于很多使用 functools.reduce() 的情形, 使用明显的 for 循环会更清晰:


    #lambda (装逼用，多数时候用def 会更加的清晰， 看场景了)
    adder = lambda x, y: x+y
    print_assign = lambda name, value: name + '=' + str(value)


    #try with git$ git config --global credential.helper wincred