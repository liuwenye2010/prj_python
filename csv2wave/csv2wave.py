"""Load & convert data from CSV file and convert into Wave file"""
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

def cmd_parser():
    parser = argparse.ArgumentParser(description="This program Load & convert data from CSV file and convert into Wave file")
    parser.add_argument("-i", dest="input" ,required=False, help="input file name")
    #parser.add_argument("-o", dest="output" ,required=False, help="output file name")
    #parser.add_argument("-t", dest="file_type" ,required=True, help="Option that for the file's suffix , e.g py")
    args = parser.parse_args()
    input_file_name  = args.input
    #output_file_name = args.output
    #file_type = args.file_type
    #print("file_type:{0}".format(file_type))
    #print("input_file_name:{0}".format(input_file_name))
    #print("output_file_name:{0}".format(output_file_name))

    if input_file_name is not None:
        pass
    else:
        input_file_name = "sound_audio_spi.csv"
        parser.print_help()
        print("[Warning] not input argument found, set input as default file")
    output_file_name = input_file_name + '.wav'
    print("[-] input is {0}, output is {1}".format(input_file_name,output_file_name))
    csv2wave_mono(16000,2,input_file_name, output_file_name) # 16KHz/16bits
    print("done")


def parse_timestamp(text):
    return datetime.strptime(text, '%Y-%m-%d %H:%M:%S')

Column = namedtuple('Column', 'src dest convert')
columns = [
    Column('MOSI', 'mosi', int),
]
def iter_records(file_name):
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
	
    for i, record in enumerate(iter_records(input_file)):
        #if i >= 10:
        #    break
		#pprint(record)
        data = struct.pack('<h', record["mosi"])
        wavef.writeframesraw( data )
    wavef.close()

if __name__ == "__main__":
    #csv2wave_mono(16000,2,"sound_audio_spi.csv","sound_audio_spi.csv.wav") # 16KHz/16bits
    cmd_parser()
