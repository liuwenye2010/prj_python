#1 os.walk current directory, and list all pl files and merge them into one file
#2 read each file's contents into one files (each file with filenames comments  ==== ** ====)
import os
import glob 
import argparse

def main():
    parser = argparse.ArgumentParser(description="This program merger the specific type of files in current folder(including sub folders) into one file")
    parser.add_argument("-i", dest="input" ,required=False, help="folder will to merge,(Otherwise will default to current working directory)")
    parser.add_argument("-o", dest="output" ,required=False, help="file name will be output,(Otherwise will default to current working directory with name output.txt)")
    parser.add_argument("-t", dest="file_type" ,required=True, help="Option that for the file's suffix , e.g py")
    args = parser.parse_args()

    file_type = args.file_type
    file_dir = args.input
    output_file_name = args.output
    print("file_type:{0}".format(file_type))
    print("file_dir:{0}".format(file_dir))
    print("output_file_name:{0}".format(output_file_name))

    if file_dir is not None and output_file_name is not None:
        print("[-] will merge {0} in  {1} and output to {2}".format( file_type, file_dir, output_file_name))
    elif file_dir is None and output_file_name is None:
        output_file_name = "output.txt"
        print("[-] will merge {0} in  {1} and output to {2}".format( file_type, file_dir, output_file_name))
        merge_files('./',file_type,'output.txt')
    else:
        parser.print_help()

def merge_files(file_dir,file_suffix,file_summary):
	file_names = os.listdir()
	print(file_names)
	file_lines = []
	if file_dir is None:
		file_dir = './'
	for parent, dir_names, file_names in os.walk(file_dir):
		for file_name in file_names:
			if file_name.endswith('.{}'.format(file_suffix)):
				print("found file:{0}".format(file_name))
				f = open(os.path.join(parent, file_name),"r", encoding = "utf8")
				line_comment_start = "\n######### >>> {0} >>>\n".format(file_name)
				file_lines.extend(line_comment_start)
				lines = f.readlines()
				file_lines.extend(lines)
				line_comment_stop = "\n######### <<< {0} <<<\n".format(file_name)
				file_lines.extend(line_comment_stop)
				f.close()
	if file_summary is None:
		file_summary='output.txt'
	with  open(file_summary,'wt') as f_summary: 
		f_summary.writelines(file_lines)

	#pl_files = glob.glob('*.pl') #if need suffix match 
	#print(pl_files)
	#fine_names = [name for name in os.listdir()]
	#print(file_names)
	for i,file_name in enumerate (file_names):
		print("filename-{0} : {1} ".format(i,file_name))

if __name__ == "__main__":
	main()
