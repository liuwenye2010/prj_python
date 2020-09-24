import os
import re
import sys
import time
import serial
#import serial.tools.list_ports
import errno
import time
import hashlib

# port_list = list(serial.tools.list_ports.comports())
# if(len(port_list) <= 0):
# 	print("No serial port connected found")
# 	sys.exit(0)
# else:
# 	ls = len(port_list)
# 	for i in range(ls):
# 		print(list(port_list[i])[0], list(port_list[i])[1])
# sys.exit(0)

try: 
	while True:
		print("Process..(CTRL + C to exit)")
		time.sleep(1)
		pass
except KeyboardInterrupt:
    print("SIGINT: Key Interrupt")