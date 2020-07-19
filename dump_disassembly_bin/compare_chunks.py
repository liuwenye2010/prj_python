#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
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


def usage():
    print("""
    1) double click this python file
    """)


def get_map_file_lines(in_map_filename, out_map_filename):
    valid = 0
    try:
        with open(out_map_filename,"w", encoding = "utf8") as f_out:
            with open(in_map_filename,"r", encoding = "utf8") as f_in:
                for l in f_in :
                    ll = l.strip() 
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

def get_all_sections_summary_lines(in_map_filename, out_map_filename):
    valid = 0
    try:
        with open(out_map_filename,"w", encoding = "utf8") as f_out:
            with open(in_map_filename,"r", encoding = "utf8") as f_in:
                for l in f_in :
                    ll = l.strip() 
                    if ll.find('Section summary for memory \'PM\':') > -1:
                        valid = 1
                    if valid == 1 and (ll.startswith('File summary:')):
                        break
                    if valid == 1 and ll != '':
                        f_out.write(l)
    except OSError as err:
        print("OS error: {0}".format(err))
        logging.critical("OS error: {0}".format(err))
        sys.exit(2)

def get_section_summary_lines(in_map_filename, out_map_filename,sec_type):
    valid = 0
    try:
        with open(out_map_filename,"w", encoding = "utf8") as f_out:
            with open(in_map_filename,"r", encoding = "utf8") as f_in:
                for l in f_in :
                    ll = l.strip() 
                    if ll.find('Section summary for memory \'{0}\':'.format(sec_type)) > -1:
                        valid = 1
                    if valid == 1 and (ll.endswith('Total')):
                        f_out.write(l)
                        break
                    if valid == 1 and ll != '':
                        f_out.write(l)
    except OSError as err:
        print("OS error: {0}".format(err))
        logging.critical("OS error: {0}".format(err))
        sys.exit(2)

def get_external_symbols_lines(in_map_filename, out_map_filename):
    valid = 0
    try:
        with open(out_map_filename,"w", encoding = "utf8") as f_out:
            with open(in_map_filename,"r", encoding = "utf8") as f_in:
                for l in f_in :
                    ll = l.strip() 
                    if ll.find('External symbols:') > -1:
                        valid = 1
                    if valid == 1 and (ll.endswith('Section summary for memory \'PM\':')):
                        f_out.write(l)
                        break
                    if valid == 1 and ll != '':
                        f_out.write(l)
    except OSError as err:
        print("OS error: {0}".format(err))
        logging.critical("OS error: {0}".format(err))
        sys.exit(2)

def get_disassembly_code_segment_lines(in_filename, out_filename, start_addr, stop_addr):
    valid = 0
    try:
        with open(out_filename,"w", encoding = "utf8") as f_out:
            with open(in_filename,"r", encoding = "utf8") as f_in:
                for l in f_in :
                    ll = l.strip() 
                    start_string = '/* {0} '.format(start_addr)
                    #start_string = "/* 0x0033a8      0x04 */    	mov m0,0x8 | mov i4,i0 /* MW 6 */"
                    if ll.find(start_string) > -1:
                        valid = 1
                    stop_string = '/* {0} '.format(stop_addr)
                    #stop_string = "/* 0x009810      0x00 */    /* MW 1 */"
                    if valid == 1 and (ll.find(stop_string)) > -1 :
                        f_out.write(l)
                        break
                    if valid == 1 and ll != '':
                        f_out.write(l)
    except OSError as err:
        print("OS error: {0}".format(err))
        logging.critical("OS error: {0}".format(err))
        sys.exit(2)

def  extract_code_segment_hex_from_diassembly_file(dir_path, disassemble_file,seg_name_str,start_addr_str, stop_addr_str):

    disassemble_segment_file = os.path.join(dir_path,'disassemble_segment_{0}.as'.format(seg_name_str))
    disassemble_segment_raw_hex_file = os.path.join(dir_path,'disassemble_segment_{0}.hex'.format(seg_name_str))

    get_disassembly_code_segment_lines(disassemble_file,disassemble_segment_file,start_addr_str ,stop_addr_str)


    with open(disassemble_segment_file, 'rt') as file:
        disassemble_segment = file.read()

    regex_segment_hex_line = r"\s+\/\*\s(0x\w+)\s+0x(\w{2,2})\s\*\/*"

    with  open(disassemble_segment_raw_hex_file,'wt') as f_hex: 
        matches = re.finditer(regex_segment_hex_line, disassemble_segment, re.MULTILINE)
        line_idx = 0 
        for matchNum, match in enumerate(matches, start=1):
            disassembly_debug = 0
            disassembly_pad   = 1
            if disassembly_debug > 0:
                if disassembly_pad > 0 : 
                    hex_addr = int(match.group(1),16)
                    if matchNum > 1 and (hex_addr - hex_addr_pre) > 1 :
                        for pad_idx in range(1 , (hex_addr - hex_addr_pre )):
                            f_hex.write("{0} : {1} : {2}\n".format(hex(line_idx),hex(hex_addr_pre+ pad_idx),"PAD_FF"))
                            print("PAD_addr:{0}".format(hex(hex_addr_pre+ pad_idx)))
                            line_idx +=1
                f_hex.write("{0} : {1} : {2}\n".format(hex(line_idx),match.group(1),match.group(2)))
                line_idx +=1
                if disassembly_pad > 0 :
                    hex_addr_pre = hex_addr
            else:
                if disassembly_pad > 0 :
                    hex_addr = int(match.group(1),16)
                    if matchNum > 1 and (hex_addr - hex_addr_pre) > 1 :
                        for pad_idx in range(1 , (hex_addr - hex_addr_pre )):
                            f_hex.write("{0}\n".format("FF"))
                f_hex.write("{0}\n".format(match.group(2)))
                if disassembly_pad > 0 :
                    hex_addr_pre = hex_addr
        #covert form hex to binary 
        disassemble_segment_raw_bin_file = os.path.join(dir_path,'disassemble_segment_{0}.bin'.format(seg_name_str))
        Popen("xxd -r -p {0} {1}".format(disassemble_segment_raw_hex_file, disassemble_segment_raw_bin_file)) # non-block



def get_disassembly_rodata_segment_lines(in_filename, out_filename, start_addr, stop_addr):
    valid = 0
    try:
        with open(out_filename,"w", encoding = "utf8") as f_out:
            with open(in_filename,"r", encoding = "utf8") as f_in:
                valid_line_cnt  = 0 
                valid_line_max = int(stop_addr,16) - int(start_addr,16) + 1
                for l in f_in :
                    ll = l.strip() 
                    #start condition 
                    start_string = '{0}'.format(start_addr)
                    #.rodata_segment YM 0x122f08     
                    ret = re.findall(r'.rodata_segment\s\w+\s{0}'.format(start_string), ll)
                    if ret :  
                        valid = 1
                        valid_line_cnt = 0 ; 
                    #stop condition 
                    if valid == 1 and (valid_line_cnt > valid_line_max ) :
                        f_out.write(l)
                        break
                    if valid == 1 and ll != '':
                        #.label filter_bank 
                        ret = re.findall(r'.label\s.*', ll)
                        if ret :
                            #pass
                            f_out.write(l)
                            #valid_line_cnt +=1
                        else:
                            f_out.write(l)
                            valid_line_cnt +=1
                        
    except OSError as err:
        print("OS error: {0}".format(err))
        logging.critical("OS error: {0}".format(err))
        sys.exit(2)

def  extract_rodata_segment_hex_from_diassembly_file(dir_path, disassemble_file,seg_name_str,start_addr_str, stop_addr_str):
    disassemble_segment_file = os.path.join(dir_path,'disassemble_segment_{0}.as'.format(seg_name_str))
    disassemble_segment_raw_hex_file = os.path.join(dir_path,'disassemble_segment_{0}.hex'.format(seg_name_str))
    get_disassembly_rodata_segment_lines(disassemble_file,disassemble_segment_file,start_addr_str ,stop_addr_str)
    pass 





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
    #logging.basicConfig(filename=log_file_name,filemode='w',level=logging.DEBUG, format=fmtStr, datefmt=dateStr)
    logging.debug('{} start'.format(str(sys.argv[0])))

    #dir_path        = os.getcwd()
    dir_path       = os.path.dirname(__file__)

    if input_file is None:
        map_file        = os.path.abspath('../bld/cape_a/tahiti_cape.map')
    else:
        map_file  = os.path.abspath(input_file)

    disassemble_file  = os.path.abspath('../bld/cape_a/tahiti_cape.as')

    if output_file is None: 
        file_summary = os.path.join(dir_path,'map_summary.txt')
    else:
        file_summary = os.path.abspath(output_file)


    map_external_symbols_file = os.path.join(dir_path,'map_external_symbols.map')
    get_external_symbols_lines(map_file,map_external_symbols_file)
    with open(map_external_symbols_file, 'rt') as file:
        external_symbols = file.read()
    
    segments_map_list = []
    regex_segment_start_stop  = r"_segment_(start|end)_(\w+)_(\w+)\s=\s(0x\w+)"
    matches = re.finditer(regex_segment_start_stop, external_symbols, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        segments_map_list.append({"seg_start_stop":match.group(1),"seg_name": match.group(2), "seg_attr": match.group(3), "seg_addr":match.group(4)})
    segments_map_list.sort(key=itemgetter('seg_name'))

    segments_map_list_merge = []
    for seg_name, items in groupby(segments_map_list, key=itemgetter('seg_name')):
        #print(seg_name) 
        for i in items:
            seg_name = i["seg_name"]
            seg_attr = i["seg_attr"]
            if i["seg_start_stop"] == "start":
                start_addr = i["seg_addr"]
            if i["seg_start_stop"] == "end":
                stop_addr = i["seg_addr"]
        segments_map_list_merge.append({"seg_name":seg_name,"seg_start":start_addr,"seg_stop":stop_addr,"seg_attr":seg_attr })

    with open("segments_map_list_merge.json", "w") as fp:
        json.dump(segments_map_list_merge, fp, indent=4)


    #extract_code_segment_hex_from_diassembly_file(dir_path, disassemble_file, "POA","0x0033a8","0x009810")
    #extract_code_segment_hex_from_diassembly_file(dir_path, disassemble_file, "POB","0x600033a8","0x60003606")
    #extract_code_segment_hex_from_diassembly_file(dir_path, disassemble_file, "POD","0x000200","0x003399")
    extract_rodata_segment_hex_from_diassembly_file(dir_path, disassemble_file, "ROA","0x122f08","0x127850")
    extract_rodata_segment_hex_from_diassembly_file(dir_path, disassemble_file, "ROB","0x60122f08","0x6012c4a0")
    extract_rodata_segment_hex_from_diassembly_file(dir_path, disassemble_file, "ROD","0x120000","0x122f00")




    for seg_name, items in groupby(segments_map_list_merge, key=itemgetter('seg_name')):
        #print (seg_name)
        #if is program : e.g POA, POB, POD, PCA, PCB, PCD, PN 
        # or if is item 's attute is PM 
        if (str(seg_name).startswith("P")): 
            #print (seg_name)
            for i in items:
                s_seg_start =  "0x{:0>6x}".format(int(i["seg_start"],16)) 
                s_seg_stop =   "0x{:0>6x}".format(int(i["seg_stop"],16)-1)
                print ("{0}==> start : {1} , stop: {2} \n".format( i["seg_name"], s_seg_start,s_seg_stop))
                extract_code_segment_hex_from_diassembly_file(dir_path, disassemble_file, i["seg_name"],s_seg_start,s_seg_stop)
        #if is rodata : e.g ROA, ROB, ROD 
        if (str(seg_name).startswith("R")): 
            print (seg_name)
            #.rodata_segment YM 0x122f08
        #else : XPA, XPB, XMA, XMB, YMA, YMB.. 

    print("done")

    logging.debug('{} end'.format(str(sys.argv[0])))

if __name__ == '__main__':
    main()