#!/usr/bin/python3
"""[example of py disassemble ]
"""
#import parser 
import dis
#import ast 
#import compileall
#import pybison 
#import PLY 

def myfunc(alist):
    return len(alist)

if __name__ == "__main__":
    dis.dis(myfunc)