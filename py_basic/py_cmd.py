import sys
import os
#from os.path import join, getsize
import time
import datetime
# import zipfile
import getopt
import math
# import copy
import re
# import webbrowser
# import sqlite3
# import fileinput
# import random
# import urllib
# import pprint
# import shelve
# import json
# import difflib
# import enum
# import functools
# import hashlib
# import itertools
import logging
# import statistics
# import timeit
# import profile
# import trace
# import tkinter as tk
# import socket
# import select
# import cgi
# import cgitb
# import http
# import smtplib
# import smtpd
# import telnetlib
import twisted  # pip install twisted
# import flask        #pip install flask simple web framework
# import unittest
# import doctest
# import subprocess
# import setuptools   #package
# import py2exe       #pip install py2exe
# import pyinstaller  #pip install pyinstaller
import argparse
import signal 


def test_argparse():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))


def show_time():
    print(now.strftime("%A, %d. %B %Y %I:%M%p"))


def btn_click_me():
    print('i was clicked!')


def call_back(event):
    print(event.x, event.y)


def usage():
    print("""
    Usage: 
    --help
    -o 
    -v 
    example: py_cmd.exe -h
    example: py_cmd.exe -o hello.txt 
    """)


def main():
    now = datetime.datetime.now()
    print(now.strftime("%A, %d. %B %Y %I:%M%p"))
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
            print("output=={}".format(str(a)))
        else:
            assert False, "unhandled option"

def test_os_system():
    exe_cmd = "arm-none-eabi-readelf -v"
    os.system(exe_cmd)



def std_lib_test():
    try:
        ##logging
        logging.basicConfig(level=logging.INFO, filename='mylog.log')
        logging.info('Start logging')
        print(sys.api_version)
        print(sys.argv)
        print(__name__)
        print('Hello World')
        now = datetime.datetime.now()
        print(now.strftime("%A, %d. %B %Y %I:%M%p"))
        logging.info(now.strftime("%A, %d. %B %Y %I:%M%p"))
        print("sin30:" + str(math.sin(30 / 180 * math.pi)))
        time.sleep(1)
        # call self define function
        show_time()
        # print(str(os.curdir()))
        # system(notepad)
        # os.system(r'C:\Program Files (x86)\Notepad++')
        # os.startfile(r'C:\Program Files (x86)\Notepad++\notepad++.exe')
        print(os.curdir)
        print(os.getcwd())  # get cwd
        ##GUI tkinter
        # top = tk.Tk()
        # btn = tk.Button()
        # btn.pack()
        # btn['text'] = 'click me '
        # btn['command'] = btn_click_me
        # lbl = tk.Label(text="this is a label text")
        # lbl.pack()
        # top.bind('<Button-1>',call_back)  # mouse left event
        # top.mainloop()

        ## re
        # prog = re.compile(pattern)
        # result = prog.match(string)
        ##is equivalent to
        # mypattern = r"(?P<first_name>\w+) (?P<last_name>\w+)"
        mypattern = r"(\w+) (\w+)"
        mystring = "Malcolm Reynolds"
        result = re.match(mypattern, mystring)
        if (result):
            print(str(result.groups()))
            print(result[0])
            print(result[1])
            print(result[2])

        mypattern = r".*_([\w]{4})_(\w+).itcl"
        # mypattern = r".*(ZAL6).*"
        mystring = r"AXXX_ASD_ZAL6_XXX.itcl"
        result = re.match(mypattern, mystring, flags=re.IGNORECASE)
        if (result):
            print(str(result.groups()))
            print(result[0])
            print(result[1])
            print(result[2])

        ##database sqlite
        conn = sqlite3.connect('food.db')
        curs = conn.cursor()
        conn.commit()
        conn.close()
        if (0):
            ##web browser
            url = 'http://docs.python.org/'
            # Open URL in a new tab, if a browser window is already open.
            webbrowser.open_new_tab(url)
            # Open URL in new window, raising the window if possible.
            webbrowser.open_new(url)
            ##socket and network framework

            # from twisted._version import __version__ as version
            # __version__ = version.short()
            print('twisted version : ' + str(twisted.__version__))

        logging.info('logging end')
        pass
    except:
        print("erorr happened")
        logging.info('erorr happened')
        sys.exit(-1)

def test_os_walk():
    #import os
    #from os.path import join, getsize
    cur_cwd = os.getcwd()
    os.path.relpath(cur_cwd)
    os.path.abspath(cur_cwd)
    sh_path = '/'.join(cur_cwd.split('\\'))
    for root, dirs, files in os.walk(sh_path):
        print(root, "consumes", end=" ")
        print(sum(os.path.getsize(os.path.join(root, name)) for name in files), end=" ")
        print("bytes in", len(files), "non-directory files")
        if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories

def test_convert_windows_path_2_linux_path():
    print("windows path ")
    sh_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    print(sh_path)

    print("linux path")
    sh_path = '/'.join(sh_path.split('\\'))  # transform the windows path to linux path
    print(sh_path)

def sig_handler(sig, f):
    print("signal hit and exit")
    exit(1)






if __name__ == '__main__':
    print("Test py_cmd start===============\n")
    #main()
    #test_os_system()
    #test_argparse()
    # std_lib_test()
    # test_os_walk()
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    for x in range(1, 10):
        time.sleep(1)
        print("sleep ..count:{0}".format(x))
        

    print("Test py_cmd end ============  \n")
