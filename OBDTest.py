import obd

# Connect to obd
connection = obd.OBD('/dev/tty.OBDII', protocol="7")

print("Connected to OBDII: "+str(connection.status()))