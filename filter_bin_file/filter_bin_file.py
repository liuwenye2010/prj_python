import csv
import wave
import struct
import math
from collections import namedtuple
from datetime import datetime
from pprint import pprint
import os
import glob 
import argparse
import os.path
import sys
import re



g_default_input_file                = "audio.csv"
g_default_column_name_to_parse      = "MOSI"
g_default_sample_rate               = 16000
g_default_sample_width              =  2

def cmd_parser():
#TODO:
    parser = argparse.ArgumentParser(description="This program is a template from console program")
    parser.add_argument("-i", dest="input" ,required=False, help="input file name (e.g audio.csv)")
    parser.add_argument("-c", dest="column_name" ,required=False, help="column name to parse (e.g MOSI)")
    parser.add_argument("-s", dest="sample_rate" ,required=False, help="sample rate for wave (e.g 16000)")
    parser.add_argument("-w", dest="sample_width" ,required=False, help="sample width for wave (1 = 8 bits, 2 = 16, 3 = invalid, 4 = 32)")
    parser.add_argument("-o", dest="output" ,required=False, help="output file name")
    
   
    args             = parser.parse_args()
    input_file_name  = args.input
    column_name      = args.column_name
    sample_rate      = args.sample_rate
    sample_width     = args.sample_width
    output_file_name = args.output

    print("input_file_name :{0}".format(input_file_name))
    print("output_file_name:{0}".format(output_file_name))

    if input_file_name is not None:
        pass
    else:
        input_file_name = g_default_input_file
        print("[Warning] not input argument for input_file_name found, set input as default ==> {0}".format(g_default_input_file))
    
    if output_file_name is not None:
        pass
    else:
        output_file_name = input_file_name + ".out"
        print("[Warning] not input argument for output_file_name found, set output_file_name as default ==> {0}".format(output_file_name))
    
    if column_name is not None:
        column_name = str(column_name) 
    else:
        column_name = g_default_column_name_to_parse
        print("[Warning] not input argument for column_name found, set column_name as default ==> {0}".format(g_default_column_name_to_parse))
        
    if sample_rate is not None:
        sample_rate = int(sample_rate)
    else:
        sample_rate = g_default_sample_rate
        print("[Warning] not input argument for sample_rate found, set sample_rate as default ==> {0}".format(g_default_sample_rate))

    if sample_width is not None:
        if sample_width  not in ['0', '1','2', '4'] :
            print("ERROR: Invalid sample_width parameter value")
            parser.print_help()
            sys.exit(-1)
        else:
            sample_width = int(sample_width)
            print("sample_width:{0}".format(sample_width))
    else:
        sample_width = g_default_sample_width # 16bit 
        print("[Warning] not input argument for sample_width found, set sample_width as default ==> {0}".format(g_default_sample_width))
      

    print("[INFO] column_name          is {0}".format(column_name))
    print("[INFO] sample_width         is {0}".format(sample_width))
    print("[INFO] sample_rate          is {0}".format(sample_rate))
    print("[INFO] input file name      is {0}".format(input_file_name))
    print("[INFO] output file name     is {0}".format(output_file_name))

    return  input_file_name, column_name, sample_width, sample_rate, output_file_name



def parse_address ():
# found out all symbols by regex 
# calc out the delta  (end -start) for same segmentation, store them in the gobals 
# read info from auto_conf get the szie for the sam segmentation 
# calc the used memory size and un-used memory size 
# generate report:  Segment:  Allocated:  Used:  Unused:
# generate the map figure (if need)
    regex = r"_segment_(.+?)_(.+?)_(.+?)\s=\s0x(.*)"

    test_str = ("    _segment_end_PCA_PM = 0x2a429\n"
        "    _segment_end_PCB_PM = 0x2d9959\n"
        "    _segment_end_PCD_PM = 0x4ce9\n"
        "    _segment_end_PMR_PM = 0x1c0\n"
        "    _segment_end_PN_PM = 0x2890d4\n"
        "    _segment_end_PR_PM = 0x201526\n"
        "    _segment_end_XDD_XM = 0xa01052b8\n"
        "    _segment_end_XPA_XM = 0x1793a0\n"
        "    _segment_end_XPB_XM = 0x1cdc8c\n"
        "    _segment_end_XS_XM = 0x110520\n"
        "    _segment_end_YMA_YM = 0x8001f9dc\n"
        "    _segment_end_YMB_YM = 0x6001fa59\n"
        "    _segment_end_YMD_YM = 0xc000\n"
        "    _segment_start_PCA_PM = 0x20000\n"
        "    _segment_start_PCB_PM = 0x2d0000\n"
        "    _segment_start_PCD_PM = 0x200\n"
        "    _segment_start_PMR_PM = 0x0\n"
        "    _segment_start_PN_PM = 0x285000\n"
        "    _segment_start_PR_PM = 0x201000\n"
        "    _segment_start_XDD_XM = 0xa0104000\n"
        "    _segment_start_XPA_XM = 0x120000\n"
        "    _segment_start_XPB_XM = 0x18d000\n"
        "    _segment_start_XS_XM = 0x110000\n"
        "    _segment_start_YMA_YM = 0x8000c000\n"
        "    _segment_start_YMB_YM = 0x6000c000\n"
        "    _segment_start_YMD_YM = 0xc000\n"
        "    _sp_end_XM = 0x1fc00\n"
        "    _sp_start_XM = 0x20000")

    matches = re.finditer(regex, test_str, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        
        print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            
            print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))


def main():
    input_file_name, column_name, sample_width, sample_rate, output_file_name =  cmd_parser()
    if 1 :# os.path.isfile(input_file_name):
        try:
            #TODO:: 
            print ("TODO:")
            parse_address()
        except KeyboardInterrupt:
            print("[INFO] User Key Interrupt exit")
            sys.exit(-1)
        else:
            pass
    else:
        print("\n[ERROR]:input file {0} is not exist !\n".format(input_file_name))
        sys.exit(-1)

    print("Done")
    parse_address()
    pass 



if __name__ == '__main__':
    main()