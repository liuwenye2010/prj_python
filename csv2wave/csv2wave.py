"""Load & convert data from CSV file and convert into Mono Wave file"""
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

default_file_to_convert = "audio.csv"
column_name_to_parse    = "MOSI"

def cmd_parser():
    global column_name_to_parse 
    global default_file_to_convert
    parser = argparse.ArgumentParser(description="This program Load & convert data from CSV file and convert into Mono Wave file")
    parser.add_argument("-i", dest="input" ,required=False, help="input file name (e.g audio.csv)")
    parser.add_argument("-c", dest="column_name" ,required=False, help="column name to parse (e.g MOSI)")
    parser.add_argument("-s", dest="sample_rate" ,required=False, help="sample rate for wave (e.g 16000)")
    parser.add_argument("-w", dest="sample_width" ,required=False, help="sample width for wave (1 = 8 bits, 2 = 16, 3 = invalid, 4 = 32)")

    #parser.add_argument("-o", dest="output" ,required=False, help="output file name")
    #parser.add_argument("-t", dest="file_type" ,required=True, help="Option that for the file's suffix , e.g py")
    args = parser.parse_args()
    input_file_name  = args.input
    column_name =  args.column_name
    sample_rate =  args.sample_rate
    sample_width =  args.sample_width
    #output_file_name = args.output
    #file_type = args.file_type
    #print("file_type:{0}".format(file_type))
    #print("input_file_name:{0}".format(input_file_name))
    #print("output_file_name:{0}".format(output_file_name))

    if input_file_name is not None:
        pass
    else:
        input_file_name = default_file_to_convert
        print("[Warning] not input argument for input_file_name found, set input as default ==> {0}".format(default_file_to_convert))
    if column_name is not None:
        column_name_to_parse = str(column_name) 
        print("column_name_to_parse is {0}".format(column_name_to_parse))
    else:
        print("[Warning] not input argument for column_name found, set column_name as default ==> {0}".format(column_name_to_parse))
        
    if sample_rate is not None:
        sample_rate = int(sample_rate)
        pass
    else:
        sample_rate = 16000 # 16KHz
    
    if sample_width is not None:
        if sample_width  not in ['0', '1','2', '4'] :
            print("ERROR: Invalid sample_width parameter value")
            parser.print_help()
            exit(1)
        else:
            sample_width = int(sample_width)
            print("sample_width:{0}".format(sample_width))
    else:
        sample_width = 2 # 16bit 

    print("[INFO] column_name_to_parse is {0}".format(column_name_to_parse))
    print("[INFO] sample_width         is {0}".format(sample_width))
    print("[INFO] sample_rate          is {0}".format(sample_rate))
    output_file_name = input_file_name + '.wav'
    print("[INFO] input is {0}, output is {1}".format(input_file_name,output_file_name))
    csv2wave_mono(sample_rate,sample_width,input_file_name, output_file_name) # 16KHz/16bits
    print("done")


def parse_timestamp(text):
    return datetime.strptime(text, '%Y-%m-%d %H:%M:%S')


def iter_records(file_name,column_name):
    Column = namedtuple('Column', 'src dest convert')
    columns = [Column(column_name, column_name, int),]
    with open(file_name, 'rt') as fp:
        reader = csv.DictReader(fp)
        for csv_record in reader:
            record = {}
            for col in columns:
                value = csv_record[col.src]
                record[col.dest] = col.convert(value)
            yield record

def csv2wave_mono(sampleRate,sampleWidth,input_file, output_file):
    wavef = wave.open(output_file,'w')
    wavef.setnchannels(1) # 1: mono
    wavef.setsampwidth(sampleWidth)  #sampleWidth -- size of data: 1 = 8 bits, 2 = 16, 3 = invalid, 4 = 32, etc... 
    wavef.setframerate(sampleRate)

    for i, record in enumerate(iter_records(input_file,column_name_to_parse)):
        #if i >= 10:
        #    break
		#pprint(record)
        data = struct.pack('<h', record[column_name_to_parse])
        wavef.writeframesraw( data )
    wavef.close()

if __name__ == "__main__":
    #csv2wave_mono(16000,2,"sound_audio_spi.csv","sound_audio_spi.csv.wav") # 16KHz/16bits
    cmd_parser()
