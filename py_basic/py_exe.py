"""
use pyinstaller to generate windows exe
Note py2exe only support python3.4 so please using pyinstaller to support python3.6
run following commands in pycharm Terminal , then you will find exe file in dist folder:

pyinstaller -F py_exe.py

"""


import sys
import os
import time
import datetime
import getopt

#print("hello exe")
#input("preess Enter:")
def usage():
    print ("""
    Usage: 
    --help
    -o 
    -v 
    example: py_exe.exe -h
    example: py_exe.exe -o hello.txt 
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


if __name__ == '__main__':
    main()
