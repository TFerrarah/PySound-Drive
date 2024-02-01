import obd

ports = obd.scan_serial()      # return list of valid USB or RF ports
print(ports)

# Choose OBDII port
while True:
    try:
        obd_port = int(input("Please choose your port [0-"+str(len(ports)-1)+"]"))
        if 0 <= obd_port <= int(len(ports)):
            break
        else:
            print("Port number is not valid. Please try again")
    except ValueError:
        print("Input not recognized. Try again")


# Create connection
connection = obd.OBD(ports[obd_port], baudrate=115200, protocol="7", fast=False) # auto-connects to USB or RF port

print(connection.status())