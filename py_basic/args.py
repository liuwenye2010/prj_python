#!/usr/bin/env python3

def main():
    hello('x', 'y', 'z')

def hello(*args):
    if len(args):
        for s in args:
            print(s)
    else: print('x.')

if __name__ == '__main__': main()
