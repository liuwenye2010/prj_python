#! /usr/bin/env python
import os 

from functools import partial
import struct
from collections import namedtuple # pack the struct member into nametuple


#remove a file 
# os.remove() removes a file.

# os.rmdir() removes an empty directory.

# shutil.rmtree() deletes a directory and all its contents.


## If file exists, delete it ##
# if os.path.isfile(myfile):
#     os.remove(myfile)
# else:    ## Show an error ##
#     print("Error: %s file not found" % myfile)

## Try to delete the file ##
# try:
#     os.remove(myfile)
# except OSError as e:  ## if failed, report it back to the user ##
#     print ("Error: %s - %s." % (e.filename, e.strerror))

## Try to remove tree; if failed show an error using try...except on screen
# try:
#     shutil.rmtree(mydir)
# except OSError as e:
#     print ("Error: %s - %s." % (e.filename, e.strerror))

def process_block(block):
    x = struct.unpack('I',block) #  return as tuple
    print ("X:{0}".format(hex(x[0])))
    pass 

def file_demo():
    #using with method

    ### file operate as txt file  
    cur_path = os.path.dirname(__file__)
    in_filename = "data_in.txt"
    #print (in_filename)
    in_filename = os.path.join(cur_path,in_filename)
    #print (in_filename)
    in_filename = os.path.abspath(in_filename)
    #print (in_filename)
    with open(in_filename,"rt", encoding = "utf8") as fp:
    #read all lines as string      
        all_data = fp.read()
    #read all lines as list fp.readlines()
        all_datalines = fp.readlines()
    #read line by line
        fp.seek(0) # seek to start to line 
        for line in iter(fp.readline, ''):
            print(line)
    #read line by line using functional method  
    #for line in in_filename:
    #    print(line)
        # do something for each line



    out_filename = "data_out.txt"  
    out_filename = os.path.join(cur_path,out_filename)
    out_filename = os.path.abspath(out_filename)
    with open(out_filename,"wt", encoding = "utf8") as fp:
    #write lines         fp.writelines()
        fp.writelines(all_datalines)
    #write all string to file 
        fp.write(all_data)
    #write line by line  fp.write()
        line = 'single line'
        fp.write(line)
    
    ### binary operation
    #file operate as binary file
    in_filename = "data_in.bin"  
    in_filename = os.path.join(cur_path,in_filename)
    in_filename = os.path.abspath(in_filename)
    with open(in_filename,"rb") as fp:
    #read all content as binary      
        all_data = fp.read()
    #read by each fixed bytes each time
        fp.seek(0) #start of file
        for block in iter(partial(fp.read, 4), b''):
            #parse as struct
            process_block(block)

    
    #write all 
    out_filename = "data_out.bin"  
    out_filename = os.path.join(cur_path,out_filename)
    out_filename = os.path.abspath(out_filename)
    with open(out_filename,"wb") as fp:
        fp.write(all_data)
    #write each fixed btyes each time
        data = b'2'
        fp.write(data)
    pass


if __name__ == "__main__":
    file_demo()
    pass