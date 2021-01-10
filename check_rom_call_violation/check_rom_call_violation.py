#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import sys
import re
import json
import getopt


def usage():
    print("""
    1) double click this python file
    2) python ./check_rom_call_violation.py    
    """)

def check_rom_call_voilation(in_filename, out_filename, rom_segments, rom_call_rules):

    symbol_ref_tables_list = []
    try:
        # 1 create symbols reference(call reference or data referecn) table list
        with open(in_filename,"r", encoding = "utf8") as f_in:
                regex_name_code_seg_symbol = r"\s{4}0x\w+\.\.0x\w+\s\(.+\)\s:\s\w+\.\w+\(.+?\)::(\S+)\s\(.*?\)\s\(.*?\)\s\(segment\s=\s(\S+)\)"
                regex_name_data_seg_symbol = r"\s{4}0x\w+\.\.0x\w+\s\(.+\)\s:\s\w+\.\w+\(.+?\)::(\S+)\s\(.*?\)\s\(segment\s=\s(\S+)\)"
                regex_without_name_code_seg_symbol = r"\s{4}0x\w+\.\.0x\w+\s\(.+\)\s:\s\w+\.\w+\(.+?\)::(\S+)\s\(.*?\)"
                #0x00100000..0x001000b3 (       180 items) : bld/cape_a/startup.o::_reset_handler (Function, Global, .text) (stack frame size = 0) (segment = PCD)
                regex_name_not_come_from_lib = r"\s{4}0x\w+\.\.0x\w+\s\(.+\)\s:\s\S+\.\w+::(\S+)\s\(.*?\)\s\(segment\s=\s(\S+)\)"
                #Called functions  :
                regex_call_func = r"\s+Called\sfunctions\s+:\s(\S+)"
                regex_call_func2 = r"^\s{36}(\S+)"
                #Referenced symbols:
                regex_ref_symbols = r"\s+Referenced\ssymbols:\s(\S+)"
                regex_ref_symbols2 = r"^\s{36}(\S+)"

                regex_call_func_hit_flag = 0
                regex_ref_symbols_hit_flag = 0
                symbol_ref_table = {}
                for l in f_in :
                    if len(l) == 0:
                        continue
                    regex_name_code_seg_symbol_hit        = re.match(regex_name_code_seg_symbol, l)
                    regex_without_name_code_seg_symbol_hit        = re.match(regex_without_name_code_seg_symbol, l)
                    regex_name_data_seg_symbol_hit        =  re.match(regex_name_data_seg_symbol, l)
                    regex_call_func_hit     = re.match(regex_call_func, l)
                    regex_ref_symbols_hit   = re.match(regex_ref_symbols, l)
                    regex_call_func_hit2     = re.match(regex_call_func2, l)
                    regex_ref_symbols_hit2   = re.match(regex_ref_symbols2, l)
                    regex_name_not_come_from_lib_hit = re.match(regex_name_not_come_from_lib, l)

                    if regex_name_code_seg_symbol_hit :
                        symbol_ref_tables_list.append(symbol_ref_table)
                        #print('{0}: ===> {1}'.format(regex_name_code_seg_symbol_hit.group(1),regex_name_code_seg_symbol_hit.group(2)))
                        symbol_ref_table = {'symbol': {'name': regex_name_code_seg_symbol_hit.group(1), 'attribute':regex_name_code_seg_symbol_hit.group(2)}, 'call_fun': [], 'ref_symbol': []}
                        continue
                    if regex_name_data_seg_symbol_hit :
                        symbol_ref_tables_list.append(symbol_ref_table)
                        #print('{0}: ===> {1}'.format(regex_name_data_seg_symbol_hit.group(1),regex_name_data_seg_symbol_hit.group(2)))
                        symbol_ref_table = {'symbol': {'name': regex_name_data_seg_symbol_hit.group(1), 'attribute':regex_name_data_seg_symbol_hit.group(2)}, 'call_fun': [], 'ref_symbol': []}
                        continue
                    if regex_name_not_come_from_lib_hit :
                        symbol_ref_tables_list.append(symbol_ref_table)
                        #print('{0}: ===> {1}'.format(regex_name_not_come_from_lib_hit.group(1),regex_name_not_come_from_lib_hit.group(2)))
                        symbol_ref_table = {'symbol': {'name': regex_name_not_come_from_lib_hit.group(1), 'attribute':regex_name_not_come_from_lib_hit.group(2)}, 'call_fun': [], 'ref_symbol': []}
                        continue
                    if regex_without_name_code_seg_symbol_hit :
                        symbol_ref_tables_list.append(symbol_ref_table)
                        #print('{0}: ===> PCD/XM'.format(regex_without_name_code_seg_symbol_hit.group(1)),)
                        symbol_ref_table = {'symbol': {'name': regex_without_name_code_seg_symbol_hit.group(1), 'attribute':'PCD/XD'}, 'call_fun': [], 'ref_symbol': []}
                        continue
                    if regex_call_func_hit :
                        #print(regex_call_func_hit.group())
                        regex_call_func_hit_flag = 1
                        regex_ref_symbols_hit_flag = 0
                        symbol_ref_table['call_fun'].append(regex_call_func_hit.group(1).strip())
                        continue
                    if regex_call_func_hit2 and  regex_call_func_hit_flag :
                        #print(regex_call_func_hit2.group())
                        symbol_ref_table['call_fun'].append(regex_call_func_hit2.group().strip())
                        continue
                    if regex_ref_symbols_hit:
                        #print(regex_ref_symbols_hit.group())
                        regex_ref_symbols_hit_flag = 1
                        regex_call_func_hit_flag  = 0
                        symbol_ref_table['ref_symbol'].append(regex_ref_symbols_hit.group(1).strip())
                        continue
                    if regex_ref_symbols_hit2 and  regex_ref_symbols_hit_flag:
                        #print(regex_ref_symbols_hit2.group())
                        symbol_ref_table['ref_symbol'].append(regex_ref_symbols_hit2.group().strip())
                        continue
                symbol_ref_tables_list.append(symbol_ref_table)

        with open("symbol_ref_tables_list.json", "w") as fp:
            json.dump(symbol_ref_tables_list, fp, indent=4)

        # 2 create symbols table for ROM segments
        #rom_segments = ['POD','POA', 'POB','ROD','ROA','ROB','XOD']
        rom_symbol_table_list  = []
        symbol_table_per_seg = {} #
        for seg in rom_segments:
            #print(seg)
            symbol_table_per_seg = {seg:[]}
            for s_i in symbol_ref_tables_list:
                if s_i :
                    if s_i['symbol']['attribute'] == seg :
                        #print(s_i['symbol']['attribute'])
                        symbol_table_per_seg[seg].append(s_i['symbol']['name'])
            rom_symbol_table_list.append(symbol_table_per_seg)

        with open("rom_symbol_table_list.json", "w") as fp:
            json.dump(rom_symbol_table_list, fp, indent=4)

        #3 iterate all the symbols in the ROM,apply the rule check
        # rom_call_rules = {
        #  "POD" : ["POD","ROD","XOD"],  # Warning:  POD call to POA in CAPE-A  and POD call to POB in CAPE-B 
        #  "POA" : ["POA","POD","ROD","ROA","XOD"],
        #  "POB" : ["POB","POD","ROD","ROB","XOD"],
        #  "ROA" : ["ROA","ROD"],
        #  "ROB" : ["ROB","ROD"]
        # }

        #covert the list to dict to make thing simple
        rom_symbol_table_dict = {}
        for r_i  in rom_symbol_table_list:
            for k,v in r_i.items():
                rom_symbol_table_dict[k] = v

        rom_call_check_segments = rom_call_rules.keys()
        with open(out_filename,"w", encoding = "utf8") as f_out:
            msg ="====== check_rom_call voilation report start ======\n"
            f_out.write(msg)
            print(msg)
            for s_i in symbol_ref_tables_list:
                if s_i:
                    symbol_2b_check   = s_i['symbol']['name'] 
                    if s_i['symbol']['attribute'] in rom_call_check_segments:
                        if s_i['call_fun'] :
                            for c_i in s_i['call_fun']:#check the reference function call
                                allow_segs =  rom_call_rules[s_i['symbol']['attribute']]
                                found_flg = 0
                                for allow_seg in allow_segs:
                                    allow_symbols_for_this_seg  = rom_symbol_table_dict[allow_seg]
                                    if c_i in allow_symbols_for_this_seg:
                                        found_flg = 1
                                if found_flg == 0:
                                    msg = "ERROR: {symbol} in {segment}can not refer to function: {call_fun} \n".format(symbol = symbol_2b_check,call_fun = c_i, segment =s_i['symbol']['attribute'] )
                                    print(msg)
                                    f_out.write(msg)
                        if s_i['ref_symbol'] :
                            for c_i in s_i['ref_symbol']:#check the reference data
                                allow_segs =  rom_call_rules[s_i['symbol']['attribute']]
                                found_flg = 0
                                for allow_seg in allow_segs:
                                    allow_symbols_for_this_seg  = rom_symbol_table_dict[allow_seg]
                                    if c_i in allow_symbols_for_this_seg:
                                        found_flg = 1
                                if found_flg == 0:
                                    msg = "ERROR: {symbol}  in {segment} can not refer to data: {data_ref} \n".format(symbol = symbol_2b_check, data_ref = c_i, segment =s_i['symbol']['attribute'] )
                                    print(msg)
                                    f_out.write(msg)
                    else:
                        pass
            msg = "===== check_rom_call voilation report end  ======\n"
            f_out.write(msg)
            print(msg)
            
    except OSError as err:
        print("OS error: {0}".format(err))
        sys.exit(2)


def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:],'hi:o:v',["help", "input=", "output=","verbose"])
    except getopt.GetoptError as err:
        usage()
    input_file = None
    output_file = None
    verbose = False
    option_padded = False
    for  o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            exit(0)
        elif o in ("-i", "--input"):
            input_file = a
            print("input_file{}".format(input_file))
        elif o in ("-o", "--output"):
            output_file = a
            print("output_file{}".format(output_file))
        else:
            assert False , "unhandle options"


    dir_path       = os.path.dirname(__file__)
    map_file_path  = os.path.abspath('../bld/cape_a')

    if input_file is None:
        map_file        = os.path.abspath('../bld/cape_a/tahiti_cape.map')
    else:
        map_file  = os.path.abspath(input_file)

    if output_file is None:
        file_summary = os.path.join(dir_path,'rom_call_voilation_report.txt')
    else:
        file_summary = os.path.abspath(output_file)

    rom_segments = ['POD','POA','POB','ROD','ROA','ROB','XOD']

    rom_call_rule_dict = {
     "POD" : ["POD","ROD","XOD"],  # Warning:  POD call to POA in CAPE-A  and POD call to POB in CAPE-B 
     "POA" : ["POA","POD","ROD","ROA","XOD"],
     "POB" : ["POB","POD","ROD","ROB","XOD"],
     "ROA" : ["ROA","ROD"],
     "ROB" : ["ROB","ROD"]
    }

    check_rom_call_voilation(map_file,file_summary,rom_segments,rom_call_rule_dict)

    print("done")

if __name__ == '__main__':
    main()