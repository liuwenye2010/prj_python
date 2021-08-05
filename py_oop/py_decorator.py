#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import functools
import time 

def add00(a,b):
    print("add00")
    print(a+b)

def add01(a, b):
    print("add01")
    start = time.time()
    print(a + b)
    time.sleep(1) #simulated the elapse time 
    est_time = time.time() - start
    print(f'time elapse:{est_time}s')


def timer01(func,*args):
    start = time.time()
    func(*args)
    time.sleep(1)
    est_time = time.time() - start
    print(f'time elapse:{est_time}s')


def timer02(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        time.sleep(1)
        est_time = time.time() - start
        print(f'time elapse:{est_time}s')
    return wrapper 


def timer04(func):
    @functools.wraps(func) 
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        time.sleep(1)
        est_time = time.time() - start
        print(f'time elapse:{est_time}s')
    return wrapper 

@timer04
def add04(a,b):
    print("add04")
    print(a+b)

def test1(func):
    def wrapper(*args, **kwargs):
        print('before test1 ...')
        func(*args, **kwargs)
        print('after test1 ...')
    return wrapper 
def test2(func):
    def wrapper(*args, **kwargs):
        print('before test2 ...')
        func(*args, **kwargs)
        print('after test2 ...')
    return wrapper 

@test2
@test1
def add03(a, b):
    print(a+b)

@timer02
def add02(a, b):
    print("add02")
    print(a+b)


if __name__ == "__main__":
    add01(1,2)
    timer01(add00,1,2)
    add02(1,2)
    print(add02.__name__)
    add03(1,2)
    add04(1,2)
    print(add04.__name__)

    pass