# Platform: Raspberry Pi
# Install python3 and pip3

sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip

# Install the required packages
pip3 install -r requirements.txt

# Write mac address to obd_mac.txt
echo "00:10:CC:4F:36:03" | sudo tee ./obd_mac.txt