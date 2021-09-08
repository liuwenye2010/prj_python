#http://people.csail.mit.edu/albert/bluez-intro/c212.html#findmyphone.py
import bluetooth

target_name = "lwy2010"
target_address = None

local_addr = bluetooth.read_local_bdaddr()
print(f"local_addr{local_addr}")

nearby_devices = bluetooth.discover_devices() # scan time about 10s 

#services= bluetooth.find_service()
#print(services)

for bdaddr in nearby_devices:
    name = bluetooth.lookup_name( bdaddr )   # and lookup_name() will sometimes return None to indicate that it couldn't determine the user-friendly name of the detected device
    print(f"{bdaddr} : {name}")
    if target_name == name:
        target_address = bdaddr
        break

if target_address is not None:
    print(f"found target bluetooth device name {target_name} with address {target_address}")
else:
    print(f"could not find target bluetooth device nearby")
