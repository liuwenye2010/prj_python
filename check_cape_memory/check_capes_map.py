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
    2) python ./check_capes_map.py  -i ../bld/cape_a/tahiti_cape.map  -o ./capes_map_summary.txt 
    3) python ./check_capes_map.py  --input ../bld/cape_a/tahiti_cape.map  --output ./capes_map_summary.txt 
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

    log_file_name  = 'check_capes_map.log'
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

    if output_file is None: 
        file_summary = os.path.join(dir_path,'map_summary.txt')
    else:
        file_summary = os.path.abspath(output_file)

    map_lines_file  = os.path.join(dir_path,'map_lines.map')
    map_text_lines_file  = os.path.join(dir_path,'map_text_lines.map')
    map_xm_lines_file = os.path.join(dir_path,'map_xm_lines.map')
    map_ym_lines_file = os.path.join(dir_path,'map_ym_lines.map')
    
    #get_map_file_lines(map_file,map_lines_file)
    get_all_sections_summary_lines(map_file,map_lines_file)
    get_section_summary_lines(map_lines_file,map_text_lines_file,'PM')
    get_section_summary_lines(map_lines_file,map_xm_lines_file,'XM')
    get_section_summary_lines(map_lines_file,map_ym_lines_file,'YM')
    


    with open(map_lines_file, 'rt') as file:
        map_lines = file.read() 

    with open(map_text_lines_file, 'rt') as file:
        map_text_lines = file.read() 

    with open(map_xm_lines_file, 'rt') as file:
        map_xm_lines = file.read() 

    with open(map_ym_lines_file, 'rt') as file:
        map_ym_lines = file.read() 


    if os.path.isfile(map_lines_file):
        os.remove(map_lines_file)

 
    #.text  File
    regex_text = r"\s(\d+)\s+(\w+\.o)\(.*\/(\w+.a)\)"
    #.bss       .data     .rodata      .stack  File
    regex_xm   = r"\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\w+\.o)\(.*\/(\w+\.a)"
    # .bss     .rodata  File
    regex_ym   = r"\s+(\d+)\s+(\d+)\s+(\w+\.o)\(.*\/(\w+\.a)"

    matches = re.finditer(regex_text, map_text_lines, re.MULTILINE)

    map_list = []
    for matchNum, match in enumerate(matches, start=1):
        map_list.append({"lib_name":match.group(3),"file_name": match.group(2), "text_size":match.group(1)})
    map_list.sort(key=itemgetter('lib_name'))

    fw_pm_size  = dict([('text', 0)])  
    caf_pm_size = dict([('text', 0)])  
    dsp_pm_size = dict([('text', 0)])
    for lib_name, items in groupby(map_list, key=itemgetter('lib_name')):
        print("======PM:{0:<16} ==== ".format(lib_name))
        for i in items:
            print("{0:<24} {1:<24} {2:<8}".format(i['lib_name'],i['file_name'],i['text_size']))
            if lib_name == "libc.a" or lib_name == "libcape2.a" or lib_name == "libcape2system.a":
                fw_pm_size["text"] += int(i['text_size'],10)
            if lib_name == "libcape2caf.a":
                caf_pm_size["text"] +=  int(i['text_size'],10)
            if lib_name == "libcape2lib.a":
                dsp_pm_size["text"] += int(i['text_size'],10)

    print('fw_pm_size : text:{0:<16}'.format(fw_pm_size["text"]))
    print('caf_pm_size: text:{0:<16}'.format(caf_pm_size["text"]))
    print('dsp_pm_size: text:{0:<16}'.format(dsp_pm_size["text"]))



    matches = re.finditer(regex_xm, map_xm_lines, re.MULTILINE)
    map_list = []
    for matchNum, match in enumerate(matches, start=1):
        map_list.append({"lib_name":match.group(6),"file_name": match.group(5), "bss_size":match.group(1),"data_size":match.group(2),"ro_data_size":match.group(3),"stack_size":match.group(4)})
    map_list.sort(key=itemgetter('lib_name'))

    fw_xm_size  = dict([('bss', 0), ('data', 0), ('rodata', 0),('stack', 0)])
    caf_xm_size = dict([('bss', 0), ('data', 0), ('rodata', 0),('stack', 0)])
    dsp_xm_size = dict([('bss', 0), ('data', 0), ('rodata', 0),('stack', 0)])

    for lib_name, items in groupby(map_list, key=itemgetter('lib_name')):
        print("======XM:{0:<16} ==== ".format(lib_name))
        for i in items:
            print("{0:<24} {1:<24} {2:<8} {3:<8} {4:<8} {5:<8}".format(i['lib_name'],i['file_name'],i['bss_size'],i['data_size'],i['ro_data_size'],i['stack_size']))
            if lib_name == "libc.a" or lib_name == "libcape2.a" or lib_name == "libcape2system.a":
                fw_xm_size['bss']       += int(i['bss_size'],10)
                fw_xm_size['data']      += int(i['data_size'],10)
                fw_xm_size['rodata']    += int(i['ro_data_size'],10)
                fw_xm_size['stack']     += int(i['stack_size'],10)
            if lib_name == "libcape2caf.a":
                caf_xm_size['bss'] += int(i['bss_size'],10)
                caf_xm_size['data'] += int(i['data_size'],10)
                caf_xm_size['rodata'] += int(i['ro_data_size'],10)
                caf_xm_size['stack'] += int(i['stack_size'],10)
            if lib_name == "libcape2lib.a":
                dsp_xm_size['bss'] += int(i['bss_size'],10)
                dsp_xm_size['data'] += int(i['data_size'],10)
                dsp_xm_size['rodata'] += int(i['ro_data_size'],10)
                dsp_xm_size['stack'] += int(i['stack_size'],10)

    print("fw_xm_size : bss:{0:<16}, data:{1:<16}, rodata:{2:<16}, stack:{3:<16}".format(fw_xm_size['bss'],fw_xm_size['data'],fw_xm_size['rodata'],fw_xm_size['stack']))
    print("caf_xm_size: bss:{0:<16}, data:{1:<16}, rodata:{2:<16}, stack:{3:<16}".format(caf_xm_size['bss'],caf_xm_size['data'],caf_xm_size['rodata'],caf_xm_size['stack']))
    print("dsp_xm_size: bss:{0:<16}, data:{1:<16}, rodata:{2:<16}, stack:{3:<16}".format(dsp_xm_size['bss'],dsp_xm_size['data'],dsp_xm_size['rodata'],dsp_xm_size['stack']))

    matches = re.finditer(regex_ym, map_ym_lines, re.MULTILINE)
    map_list = []
    for matchNum, match in enumerate(matches, start=1):
        map_list.append({"lib_name":match.group(4),"file_name": match.group(3), "bss_size":match.group(1),"ro_data_size":match.group(2)})
    map_list.sort(key=itemgetter('lib_name'))

    fw_ym_size  = dict([('bss', 0), ('rodata', 0)]) 
    caf_ym_size = dict([('bss', 0), ('rodata', 0)]) 
    dsp_ym_size = dict([('bss', 0), ('rodata', 0)])  
    for lib_name, items in groupby(map_list, key=itemgetter('lib_name')):
        print("======YM:{0:<16} ==== ".format(lib_name))
        for i in items:
            print("{0:<24} {1:<24} {2:<8} {3:<8}".format(i['lib_name'],i['file_name'],i['bss_size'],i['ro_data_size']))
            if lib_name == "libc.a" or lib_name == "libcape2.a" or lib_name == "libcape2system.a":
                fw_ym_size['bss']       += int(i['bss_size'],10)
                fw_ym_size['rodata']      += int(i['ro_data_size'],10)
            if lib_name == "libcape2caf.a":
                caf_ym_size['bss']       += int(i['bss_size'],10)
                caf_ym_size['rodata']      += int(i['ro_data_size'],10)
            if lib_name == "libcape2lib.a":
                dsp_ym_size['bss']       += int(i['bss_size'],10)
                dsp_ym_size['rodata']      += int(i['ro_data_size'],10)
    print("fw_ym_size : bss:{0:<16}, rodata:{1:<16}".format(fw_ym_size['bss'],fw_xm_size['rodata']))
    print("caf_ym_size: bss:{0:<16}, rodata:{1:<16}".format(caf_ym_size['bss'],caf_xm_size['rodata']))
    print("dsp_ym_size: bss:{0:<16}, rodata:{1:<16}".format(dsp_ym_size['bss'],dsp_xm_size['rodata']))

    # with  open(file_summary,'wt') as f_summary: 
    #     f_summary.write("======== >{:^32} <===MAP Summary====\n\n".format(os.path.basename(map_file)))
    #     sum_total_text_size = 0
    #     sum_total_rodata_size =0
    #     sum_total_data_size = 0
    #     sum_total_bss_size = 0 
    #     sum_total_memory_exclude_fill_size = 0

    #     for file_name, items in groupby(map_list, key=itemgetter('file_name')):
    #         f_summary.write("file_name:\t{:<32}\n".format(file_name))
    #         sum_file_text_size = 0
    #         sum_file_rodata_size =0
    #         sum_file_data_size = 0
    #         sum_file_bss_size = 0 
    #         sum_file_total_size = 0
    #         for i in items:
    #             if i["type"] == '.text':
    #                 sum_file_text_size += int(i["symbol_size"],16)
    #             if i["type"] == '.rodata':
    #                 sum_file_rodata_size += int(i["symbol_size"],16)
    #             if i["type"] == '.data':
    #                 sum_file_data_size += int(i["symbol_size"],16)
    #             if i["type"] == '.bss':
    #                 sum_file_bss_size += int(i["symbol_size"],16)
    #         sum_file_total_size = sum_file_text_size + sum_file_rodata_size  + sum_file_data_size + sum_file_bss_size
    #         f_summary.write("\ttext_size:\t{:>16}\t\n".format(sum_file_text_size))
    #         f_summary.write("\trodata_size:\t{:>16}\t\n".format(sum_file_rodata_size))
    #         f_summary.write("\tdata_size:\t{:>16}\t\n".format(sum_file_data_size))
    #         f_summary.write("\tbss_size:\t{:>16}\t\n".format(sum_file_bss_size))
    #         f_summary.write("\ttotal_size:\t{:>16}\t\n".format(sum_file_total_size))
    #         sum_total_text_size += sum_file_text_size
    #         sum_total_rodata_size += sum_file_rodata_size
    #         sum_total_data_size += sum_file_data_size
    #         sum_total_bss_size += sum_file_bss_size
    #     sum_total_memory_exclude_fill_size = sum_total_text_size + sum_total_rodata_size + sum_total_data_size + sum_total_bss_size

    #     f_summary.write("\nsum_total_text_size\t: {:>16}\n".format(sum_total_text_size))
    #     f_summary.write("\nsum_total_rodata_size\t: {:>16}\n".format(sum_total_rodata_size))
    #     f_summary.write("\nsum_total_data_size\t: {:>16}\n".format(sum_total_data_size))
    #     f_summary.write("\nsum_total_bss_size\t: {:>16}\n".format(sum_total_bss_size))
    #     f_summary.write("\nsum_total_memory_exclude_fill_size\t: {:>16}\n".format(sum_total_memory_exclude_fill_size))
    #     f_summary.write("========{:<32}=======\n".format("mcu map_summary end"))
    #     f_summary.close()
		
    #     Popen("notepad {}".format(file_summary)) # non-block
    print("done")

    logging.debug('{} end'.format(str(sys.argv[0])))

if __name__ == '__main__':
    main()