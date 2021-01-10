#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# the above tag defines encoding for this document and is for Python 2.x compatibility
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


def usage():
    print("""
    1) double click
    2) python ./check_mcu_map.py  -i ../build/mcu_ns.map  -o ./mcu_ns_summary.txt 
    3) python ./check_mcu_map.py  --input ../build/mcu_ns.map  --output ./mcu_ns_summary.txt 
    """)


def get_map_file_lines(in_map_filename, out_map_filename):
    valid = 0
    try:
        with open(out_map_filename,"w", encoding = "utf8") as f_out:
            with open(in_map_filename,"r", encoding = "utf8") as f_in:
                for l in f_in :
                    ll = l.strip() # myline.rstrip('\n')
                    if ll.find('Memory Configuration') > -1:
                        valid = 1
                    if valid == 1 and (ll.startswith('.debug_') or ll.startswith('.debug_info')):
                        break
                    if valid == 1 and ll != '':
                        f_out.write(l)
    except OSError as err:
        print("OS error: {0}".format(err))
        logging.critical("OS error: {0}".format(err))
        sys.exit(2)

def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:],'hi:o:v',["help", "input=", "output="])
    except getopt.GetoptError as err:
        usage()
    input_file = None
    output_file = None 
    verbose = False
    for  o, a in opts: 
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit(-1)
        elif o in ("-i", "--input"):
            input_file = a
            print("input_file{}".format(input_file))
            logging.debug("input_file{}".format(input_file))
        elif o in ("-o", "--output"):
            output_file = a
            print("output_file{}".format(output_file))
            logging.debug("output_file{}".format(output_file))
        else:
            assert False , "unhandle options"

    log_file_name  = 'check_mcu_map.log'
    fmtStr = "%(asctime)s: %(levelname)s: %(funcName)s Line:%(lineno)d %(message)s"
    dateStr = "%m/%d/%Y %I:%M:%S %p"
    logging.basicConfig(filename=log_file_name,filemode='w',level=logging.DEBUG, format=fmtStr, datefmt=dateStr)
    logging.debug('{} start'.format(str(sys.argv[0])))

    ##(1) step 1 script out needed map lines (txt format) store to a new file
    dir_path        = os.getcwd()
    #path_file = os.path.join(dir_path,'mcu_ns.map')
    if input_file is None:
        map_file        = os.path.abspath('../build/mcu_ns.map')
    else:
        map_file  = os.path.abspath(input_file)

    if output_file is None: 
        file_summary = os.path.join(dir_path,'map_summary.txt')
    else:
        file_summary = os.path.abspath(output_file)

    map_lines_file  = os.path.join(dir_path,'map_lines.map')
    get_map_file_lines(map_file,map_lines_file)


    with open(map_lines_file, 'rt') as file:
        map_lines = file.read() #file.read().replace('\n', '')

    if os.path.isfile(map_lines_file):
        os.remove(map_lines_file)
        
    ##(2) step 2 find all matched using re (generator)
    regex_all = r"([.text|.rodata|.data|.bss]+)\.(\S*)\s*(0x[0-9a-zA-A]*)\s*(0x[0-9a-zA-A]*)\s*\S*(\(.*?\))"
    matches = re.finditer(regex_all, map_lines, re.MULTILINE | re.DOTALL )

    ##(3) step 3 create dict list 
    map_list = []
    for matchNum, match in enumerate(matches, start=1):
        map_list.append({"type":match.group(1),"file_name": match.group(5), "symbol_name": match.group(2), "symbol_size":match.group(4)})
        # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        # for groupNum in range(0, len(match.groups())):
        #     groupNum = groupNum + 1
        #     print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
    ##(3.1) store dict list to json file for debug purpose 
    with open("map_list.json", "w") as fp:
        json.dump(map_list, fp, indent=4)

    ##(4) sort the dict in the list by Key 'file_name'
    map_list.sort(key=itemgetter('file_name'))

    ##(5) calculate the size of [.text | .rodata |.data |.bss] for each file by using groupby
    with  open(file_summary,'wt') as f_summary: 
        f_summary.write("======== >{:^32} <===MAP Summary====\n\n".format(os.path.basename(map_file)))
        sum_total_text_size = 0
        sum_total_rodata_size =0
        sum_total_data_size = 0
        sum_total_bss_size = 0 
        sum_total_memory_exclude_fill_size = 0

        for file_name, items in groupby(map_list, key=itemgetter('file_name')):
            #print("file_name:{}".format(file_name))
            f_summary.write("file_name:\t{:<32}\n".format(file_name))
            sum_file_text_size = 0
            sum_file_rodata_size =0
            sum_file_data_size = 0
            sum_file_bss_size = 0 
            sum_file_total_size = 0
            for i in items:
                #print(' ', i)
                if i["type"] == '.text':
                    sum_file_text_size += int(i["symbol_size"],16)
                if i["type"] == '.rodata':
                    sum_file_rodata_size += int(i["symbol_size"],16)
                if i["type"] == '.data':
                    sum_file_data_size += int(i["symbol_size"],16)
                if i["type"] == '.bss':
                    sum_file_bss_size += int(i["symbol_size"],16)
            sum_file_total_size = sum_file_text_size + sum_file_rodata_size  + sum_file_data_size + sum_file_bss_size
            f_summary.write("\ttext_size:\t{:>16}\t\n".format(sum_file_text_size))
            f_summary.write("\trodata_size:\t{:>16}\t\n".format(sum_file_rodata_size))
            f_summary.write("\tdata_size:\t{:>16}\t\n".format(sum_file_data_size))
            f_summary.write("\tbss_size:\t{:>16}\t\n".format(sum_file_bss_size))
            f_summary.write("\ttotal_size:\t{:>16}\t\n".format(sum_file_total_size))
            sum_total_text_size += sum_file_text_size
            sum_total_rodata_size += sum_file_rodata_size
            sum_total_data_size += sum_file_data_size
            sum_total_bss_size += sum_file_bss_size
        sum_total_memory_exclude_fill_size = sum_total_text_size + sum_total_rodata_size + sum_total_data_size + sum_total_bss_size

        f_summary.write("\nsum_total_text_size\t: {:>16}\n".format(sum_total_text_size))
        f_summary.write("\nsum_total_rodata_size\t: {:>16}\n".format(sum_total_rodata_size))
        f_summary.write("\nsum_total_data_size\t: {:>16}\n".format(sum_total_data_size))
        f_summary.write("\nsum_total_bss_size\t: {:>16}\n".format(sum_total_bss_size))
        f_summary.write("\nsum_total_memory_exclude_fill_size\t: {:>16}\n".format(sum_total_memory_exclude_fill_size))
        f_summary.write("========{:<32}=======\n".format("mcu map_summary end"))
        f_summary.close()

        ## step 6  open the summary file with notepad++ or webbroser 
        #subprocess.run("notepad {}".format(file_summary),shell=True) # block
        #webbrowser.open('file://' + os.path.realpath(file_summary))  # non-block
        Popen("notepad {}".format(file_summary)) # non-block
        #os.startfile(file_summary) #non-block, only for windows system
        
    print("done")
    logging.debug('{} end'.format(str(sys.argv[0])))
    #os.system("notepad {}".format(log_file_name)) #block ,not prefer 
    #Popen("notepad {}".format(log_file_name)) # non-block

if __name__ == '__main__':
    main()