#! /usr/bin/python
import zlib 
import binascii 
import hashlib 
import os
"""

Python is doing a signed 32-bit CRC 
Just a note: in Python3, this was changed so that it runs an unsigned CRC
https://docs.python.org/3/library/binascii.html#binascii.crc32
Changed in version 3.0: Always returns an unsigned value. 
To generate the same numeric value across all Python versions and platforms, 
use crc32(data) & 0xffffffff.

One quick way to convert from 32-bit signed to 32-bit unsigned is:*
>>> -1311505829 % (1<<32)
2983461467
>>>  hex(int('-0x1',16)% (1<<32))
"""

def crc32_demo1 (): 
    print("PY:CRC32")
    crc_1 = binascii.crc32(b'hello-world')& 0xffffffff
    crc_2 = zlib.crc32(b'hello-world') & 0xffffffff
    print('binascii crc32 = {:#010x}'.format(crc_1))
    print('zlib crc32     = {:#010x}'.format(crc_2))

def crc32_demo2 (file_in): 
    with open(file_in,'rb') as fp:
        crc_res = zlib.crc32(fp.read()) & 0xffffffff
        print('[crc32]\n', hex(crc_res))


def md5_demo(file_in):
    with open(file_in,'rb') as fp: 
        md5func = hashlib.md5()
        md5func.update(fp.read()) 
        md5_res = md5func.hexdigest()
        print('[md5]\n', md5_res)

def sha1_demo(file_in):
    with open(file_in,'rb') as fp: 
        sha1func = hashlib.sha1()
        sha1func.update(fp.read())
        sha1_res =  sha1func.hexdigest()
        print('[sha1]\n', sha1_res)


if __name__ == "__main__":
    dir_path       = os.path.dirname(__file__)
    file_in        = os.path.join(dir_path,'data.bin')
    crc32_demo1()
    crc32_demo2(file_in) #32bit
    print("the crc32 value from the crc32.c should same as python result [crc32 data.bin]")
    md5_demo(file_in)  #128bit
    sha1_demo(file_in) #160bit
	
    pass

