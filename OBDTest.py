import obd

connection = obd.OBD('/dev/tty.OBDII', 9600, protocol=7, fast=False)

print(connection.status())