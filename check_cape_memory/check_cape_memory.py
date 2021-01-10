#!/usr/bin/env python3
import os
import argparse
import os.path
import sys
import re
import json 
from operator import itemgetter
from itertools import groupby
import subprocess
from subprocess import Popen

g_default_input_map_file                     = "example.map.in"
g_default_input_autoconf_file                = "autoconf.h"
g_debug_mode = 0

def cmd_parser():
    parser = argparse.ArgumentParser(description="This program is for checking the cape's memory map")
    parser.add_argument("-i","--input", dest="input" ,required=False, nargs=2, help="input map file name (e.g tahiti_cape.map) and autoconf file (e.g autoconf.h)")
    parser.add_argument("-o","--output", dest="output" ,required=False, help="output file name")
    
    if (g_debug_mode):
        args                     = parser.parse_args('-i example.map.in autoconf.h -o segment_resutls.map'.split())
    else:
        args                     = parser.parse_args()

    if args.input is not None:
        if len(args.input) == 2:
            input_map_file = args.input[0]
            input_autoconf_file = args.input[1]
            pass
        else:
            raise ValueError('Argument input with wrong number of values')
    else:
        input_map_file     = g_default_input_map_file
        print("[Warning] not input argument for input_map_file found, set input as default ==> {0}".format(input_map_file))
        input_autoconf_file = g_default_input_autoconf_file
        print("[Warning] not input argument for input_autoconf_file found, set input as default ==> {0}".format(input_autoconf_file))
    
    if args.output is not None:
        output_file = args.output
        pass
    else:
        output_file = os.path.join(os.path.dirname(__file__),os.path.basename(input_map_file)) + "_segments_usage.map"
        print("[Warning] not input argument for output_file_name found, set output_file_name as default ==> {0}".format(output_file))
    
    print("input_map_file      :{0}".format(input_map_file))
    print("input_autoconf_file :{0}".format(input_autoconf_file))
    print("output_file         :{0}".format(output_file))

    return  input_map_file, input_autoconf_file, output_file


def get_file_lines_between_strs(in_filename, out_filename, start_str, stop_str):
    valid = 0
    try:
        with open(out_filename,"w", encoding = "utf8") as f_out:
            with open(in_filename,"r", encoding = "utf8") as f_in:
                for l in f_in :
                    ll = l.strip()
                    if ll.find(str(start_str)) > -1:
                        valid = 1
                    if valid == 1 and (ll.startswith(str(stop_str))):
                        break
                    if valid == 1 and ll != '':
                        f_out.write(l)
    except OSError as err:
        print("OS error: {0}".format(err))
        sys.exit(2)

def get_file_lines_regex(in_filename, out_filename, regex_str):
    valid = 0
    try:
        with open(out_filename,"w", encoding = "utf8") as f_out:
            with open(in_filename,"r", encoding = "utf8") as f_in:
                in_file_content = f_in.read()
                p_re = re.compile(regex_str)
                out_file_lines = p_re.findall(in_file_content)
                f_out.writelines(out_file_lines)
                #print(''.join(out_file_lines))
                out_str = ''.join(out_file_lines)
                return out_str
    except OSError as err:
        print("OS error: {0}".format(err))
        sys.exit(2)


def parse_autoconf_address (test_str):
    regex = r"CONFIG_SEGMENT.*?_(.*?)_SIZE\s(0x.*)"
    matches = re.finditer(regex, test_str, re.MULTILINE)
    configs_list = []
    for matchNum, match in enumerate(matches, start=1):
        configs_list.append({"seg_sub_type":match.group(1),"config_size":match.group(2)})
    if (g_debug_mode):
        with open("configs_list.json", "w") as fp:
            json.dump(configs_list, fp, indent=4)
    return configs_list

def parse_map_address (test_str):
# found out all symbols by regex 
# sorted by type and addr (make full use of stable sort)
# calc out the delta (end -start) for same segmentation
# read info from auto_conf get the szie for the segments
# generate report:  Segment:  Allocated:  Used:  Unused:
# generate the map figure (need third-party lib, not recommanded)
    regex = r"_segment_(.+?)_(.+?)_(.+?)\s=\s(0x.*)"
    matches = re.finditer(regex, test_str, re.MULTILINE)

    map_list = []
    for matchNum, match in enumerate(matches, start=1):
        map_list.append({"type":match.group(3),"sub_type": match.group(2), "pos": match.group(1), "addr": match.group(4)})
    map_list.sort(key= lambda x: int(x['addr'],16)) #addr
    map_list.sort(key=itemgetter('type'))           #type
    if (g_debug_mode):
        with open("map_list.json", "w") as fp:
            json.dump(map_list, fp, indent=4)

    segments_map = []
    for sub_type,items in groupby(map_list, key=itemgetter('sub_type')):
        seg_type     = ""
        seg_sub_type = sub_type
        seg_start    = 0
        seg_end      = 0
        seg_size     = 0
    
        for item in items:
            if (g_debug_mode):
                #print("type:{0:<10},sub_type:{1:<10}, pos:{2:<10},addr:{3:<10}".format(item['type'],item['sub_type'],item['pos'],item['addr']))
                pass
            if item['pos'] == 'start':
                seg_start  = int(item['addr'],16)
                seg_type  = item['type']
            if item['pos'] == 'end':
                seg_end    = int(item['addr'],16)
        seg_size   = seg_end - seg_start
        segments_map.append({"seg_type": seg_type, "seg_sub_type":seg_sub_type, "seg_start": hex(seg_start), "seg_end":hex(seg_end),"seg_size":hex(seg_size)})
        if (g_debug_mode):
            print("type: {0:<4}, sub_type: {1:<4}, seg range: 0x{2:08x} ~ 0x{3:08x} , used size: {4:<8} bytes".format(seg_type, seg_sub_type,seg_start,seg_end,seg_size))
            with open("segments_map.json", "w") as fp:
                json.dump(segments_map, fp, indent=4)
    return segments_map

def main():
    input_map_file,input_autoconf_file, output_file =  cmd_parser()
    try:
        #print ("Exract the txt content from files")
        dir_path       = os.path.dirname(__file__)
        if (g_debug_mode):
            input_map_file     =  os.path.join(dir_path,input_map_file)
        map_lines_file     =  os.path.join(dir_path,'map_lines.map')
        get_file_lines_between_strs(input_map_file,map_lines_file,'External symbols:','Section summary for memory')
        #get_file_lines_regex(input_map_file,map_lines_file,r'^External symbols:.*Section summary for memory')

        with open(map_lines_file, 'rt') as file_in:
            map_lines = file_in.read()
        if os.path.isfile(map_lines_file):
            os.remove(map_lines_file)
            
        if (g_debug_mode):
            input_autoconf_file     =  os.path.join(dir_path,input_autoconf_file)
        autoconf_lines_file  = os.path.join(dir_path,'autoconf_lines.map')
        autoconf_lines = get_file_lines_regex(input_autoconf_file, autoconf_lines_file , r'CONFIG_SEGMENT_.*?\n')
        if (g_debug_mode):
            with open(autoconf_lines_file, 'rt') as file_in:
                autoconf_lines = file_in.read()
        if os.path.isfile(autoconf_lines_file):
            os.remove(autoconf_lines_file)
        #print ("Parse the txt content")
        segments_map    = parse_map_address(map_lines)
        segments_confgs = parse_autoconf_address(autoconf_lines)
        total_unused = 0 
        with open(output_file, 'wt') as f_out:
            out_str = "== Memory Segementation Usage Summary =="
            print(out_str)
            f_out.write(out_str +'\n')
            for map_item in segments_map:
                for config_item in segments_confgs:
                    flag = 0
                    #PCD,PCA,PCB,YMD,XS,PN  (no PR in config_item)
                    if map_item['seg_sub_type'] == config_item['seg_sub_type']:
                        flag = 1 
                    #YMA == YMX
                    if ((map_item['seg_sub_type'] == 'YMA') and (config_item['seg_sub_type'] == 'YMX')):
                        flag = 1
                    #YMB== YMX
                    if ((map_item['seg_sub_type'] == 'YMB') and (config_item['seg_sub_type'] == 'YMX')):
                        flag = 1
                    #XPA == XMA
                    if ((map_item['seg_sub_type'] == 'XPA') and (config_item['seg_sub_type'] == 'XMA')):
                        flag = 1
                    #XPB == XMB 
                    if ((map_item['seg_sub_type'] == 'XPB') and (config_item['seg_sub_type'] == 'XMB')):
                        flag = 1
                    #XDD == XMD
                    if ((map_item['seg_sub_type'] == 'XDD') and (config_item['seg_sub_type'] == 'XMD')):
                        flag = 1
                    
                    if flag == 1: 
                        map_item['config_size'] = config_item['config_size']
                        map_item['unused_size'] = hex(int(map_item['config_size'],16) - int(map_item['seg_size'],16)) 
                        total_unused += int(map_item['unused_size'],16)
                        map_item['unused_size'] = map_item['unused_size'] + "(" + str(int(map_item['unused_size'],16)) + ")"
                        map_item['seg_size'] = map_item['seg_size'] + "(" + str(int(map_item['seg_size'],16)) + ")"
                        out_str = "type: {0:<4}, sub_type: {1:<4}, seg range: 0x{2:08x} ~ 0x{3:08x} , used size: {4:<16} , config size: {5:<8}, unused size: {6:<16} bytes".format( map_item['seg_type'], map_item['seg_sub_type'],int(map_item['seg_start'],16),int(map_item['seg_end'],16),map_item['seg_size'],map_item['config_size'],map_item['unused_size'])
                        print(out_str)
                        f_out.write(out_str+'\n')
            out_str  = "== Total Unused(Hole) Memory: {0:<8} bytes ==".format(total_unused)
            print (out_str)
            f_out.write(out_str+'\n')
            f_out.close()
        if (g_debug_mode):
            with open("segments_map_updated.json", "w") as fpx:
                json.dump(segments_map, fpx, indent=4)
            Popen("notepad {}".format(output_file)) # non-block
        
    except KeyboardInterrupt:
        print("[INFO] User Key Interrupt exit")
        sys.exit(-1)
    except OSError as err:
        print("[ERR] OS error: {0}".format(err))
    #except ValueError as err:
    #    print("[ERR] ValueError: {0}".format(err))
    #except:
    #    print("[ERR] Unknown error")
    finally:
        pass
    print("Done")
    pass 


if __name__ == '__main__':
    main()