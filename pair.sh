#!/usr/bin/expect -f

# Runs bluetoothctl and attempts to connect with bluetooth device
# If connection fails, tries to unpair, pair and then connect again
# My specific device apparently can't be paired to multiple hosts, so it needs this

# Change this to whatever your device's bluetooth ID is
set ID "00:10:CC:4F:36:03"

spawn "bluetoothctl"
expect "# "
send "power on\n"
expect "# "
send "trust $ID\n"
expect "# "
send "connect $ID\n"
expect {
    "Failed to connect: org.bluez.Error.Failed" {
        send "remove $ID\n"
        expect "[NEW] Device $ID"
        send "pair $ID\n"
        expect "Pairing succesful"
        send "connect $ID\n"
    }
}
expect "Connection successful"
expect "# "
send "quit\n"
expect eof
exit