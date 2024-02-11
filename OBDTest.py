import obd
import subprocess

# read ObdII mac from file
with open("obd_mac.txt", "r") as file:
    OBD_MAC = file.read().strip()

# Connect to OBDII
p = subprocess.Popen("sudo rfcomm connect hci0 "+OBD_MAC, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Create connection
ports = obd.scan_serial()
print(ports)
connection = obd.OBD(ports[0], baudrate=115200, protocol="7", fast=False)
