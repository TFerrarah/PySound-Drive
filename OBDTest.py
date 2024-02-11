import obd

# Connect to obd
connection = obd.OBD('/dev/tty.OBDII', baudrate=115200, protocol="7", fast=False)

print("Connected to OBDII: "+str(connection.status()))