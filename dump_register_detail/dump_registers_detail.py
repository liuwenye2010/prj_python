import os 
import sys 
import re
from operator import itemgetter
from itertools import groupby
import subprocess
from subprocess import Popen
import json 
import webbrowser
import logging
import getopt
#import tkinter 
#import sqlit3 
#import configparser 
#import argparser 

#echo set argv {%*};source i2c_flash.tcl | tclkitsh-8.5.9-win32.upx.exe
#os.system('echo "hello command" > hello.txt ')
#os.system('echo set argv {%*};source test.tcl | tclkitsh-8.5.9-win32.upx.exe')
cmd = 'echo set argv {%*};source test.tcl | tclkitsh-8.5.9-win32.upx.exe'
cmd_out = subprocess.check_output(cmd, encoding = "utf8", shell=True).strip()
file_cmd_out = os.path.abspath('./cmd_out_dump.txt')
with  open(file_cmd_out,'wt') as f_cmd_out:
    f_cmd_out.writelines(cmd_out)

rego =  os.path.abspath('./rego')
print(rego)
register_dump_file =  os.path.abspath('./cmd_out_dump.txt')
print(register_dump_file)
with open(register_dump_file, 'rt') as file:
        register_lines = file.read() #file.read().replace('\n', '')

regex = r"@(0x[0-9a-zA-Z]{8})==(0x[0-9a-zA-Z]{8})"

test_str = register_lines 
# test_str = ("@0x42022c18==0x04880488\n"
# 	"@0x42022c1c==0x009c03ff\n"
# 	"@0x42022c38==0x00000000\n"
# 	"@0x42022c3c==0x20000000\n\n")

matches = re.finditer(regex, test_str, re.MULTILINE)
dump = []
for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    reg_addr = match.group(1)
    reg_val  = match.group(2)
    dump.append(str(subprocess.check_output( rego + ' ' + str(reg_addr) +  ' ' + str(reg_val)), encoding = "utf8").strip())
#    print(subprocess.check_output( rego + ' ' + str(reg_addr) +  ' ' + str(reg_val)).decode("utf-8").strip())
file_summary = os.path.abspath('./register_dump.map')
with  open(file_summary,'wt') as f_summary:
    for l in dump:
        f_summary.write('\n')
        for ll in str(l):
            f_summary.write(ll.strip('\n'))

os.startfile(file_summary)
print("done")
