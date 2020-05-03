
import os 
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