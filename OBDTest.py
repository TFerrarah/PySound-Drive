import time
from OBDHandler import OBDHandler

p = OBDHandler()
MAX_RPM = 5000

try:
    while True:
        time.sleep(0.05)

        # Get values
        frequencies = p.get_frequencies()
        
        # speed frequency (Hz) = frequencies["speed"]

        # Apply lpf

        


except KeyboardInterrupt:
    print("cya")

