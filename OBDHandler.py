import obd
import math

obd.logger.setLevel(obd.logging.DEBUG)

MAX_SPEED = 150

class OBDHandler():
    def __init__(self):

        ports = obd.scan_serial()      # return list of valid USB or RF ports
        print(ports)
        
        # Choose OBDII port
        while True:
            try:
                self.obd_port = int(input("Please choose your port [0-"+str(len(ports)-1)+"]"))
                if 0 <= self.obd_port <= int(len(ports)):
                    break
                else:
                    print("Port number is not valid. Please try again")
            except ValueError:
                print("Input not recognized. Try again")


        # Create connection
        self.connection = obd.OBD(ports[self.obd_port], baudrate=9600, protocol="7", fast=False) # auto-connects to USB or RF port

        # Set max RPM
        while True:
            try:
                self.max_rpm = int(input("Please enter your car's redline RPM [e.g. 4500, 8000]: "))
                if 0 <= self.max_rpm <= 15000:
                    break
                else:
                    print("Max RPM must be between 0 - 15000")
            except ValueError:
                print("Input not recognized. Try again")

        # Reset values
        self.speed = 0
        self.rpm = 0
        self.pedal = 0

    def get_speed(self):
        cmd = obd.commands.SPEED
        response = self.connection.query(cmd)
        return response.value.to("kph").magnitude

    def get_rpm(self):
        cmd = obd.commands.RPM
        response = self.connection.query(cmd)
        return response.value.magnitude
    
    def get_pedal(self):
        cmd = obd.commands.ACCELERATOR_POS_D
        # cmd = obd.commands[1][17] # Uncomment for emulator use only
        response = self.connection.query(cmd)
        # response_percent = response.value.magnitude * 0.01
        response_percent = (response.value.magnitude-31.5)*0.02 # Slightly modified lesageethan's percentage formula for Carmony
        if response_percent<0:
            return 0
        return response_percent# user-friendly unit conversions

    def refresh_values(self): # Also taken from lesageethan's Carmony
        self.speed = self.get_speed()
        self.rpm = self.get_rpm()
        self.pedal = self.get_pedal()
    
    def pedal_to_freq(self, percentage):
        return -31005.6*percentage**2+51178*percentage-41.8572 # Formula calculated using https://www.dcode.fr/function-equation-finder
    
    def rpm_to_freq(self, percentage):
        return 68241*percentage-13525.3 # Formula calculated using https://www.dcode.fr/function-equation-finder
    
    def speed_to_freq(self, percentage):
        return 1874.42*math.log(2079.27*percentage+0.0331104)+6587.76 # Formula calculated using https://www.dcode.fr/function-equation-finder
    
    def speed_to_vol(self, percentage):
        r = 5.49451*percentage**2+3.9011*percentage
        if r > 1 : r=1
        return r

    def rpm_to_vol(self, percentage):
        r = 25.1634*percentage**0.0395332-23.8083
        if r < 0 : r = 0 
        elif r > 1 : r = 1
        return r
    
    def pedal_to_vol(self, percentage):
        return percentage

    
    def normalize_value(self, curr, max_value):
        curr = max(0, curr)
        max_value = max(0, max_value)

        normalized_value = curr / max_value

        normalized_value = min(1, max(0, normalized_value))

        return normalized_value

    def get_percentages(self):
        self.refresh_values()
        return {
            "speed": self.normalize_value(self.speed, MAX_SPEED), # Speed_normalized = 2/300 * real speed
            "rpm": self.normalize_value(self.rpm, self.max_rpm),
            "pedal": self.pedal
        }
    
    def get_frequencies(self):
        self.refresh_values() # Auto refresh values
        return {
            "speed": self.speed_to_freq(self.normalize_value(self.speed, MAX_SPEED)),
            "rpm": self.rpm_to_freq(self.normalize_value(self.rpm, self.max_rpm)),
            "pedal": self.pedal_to_freq(self.pedal)
        }
    
    def get_volumes(self):
        self.refresh_values() # Auto refresh values
        return {
            "speed": self.speed_to_vol(self.normalize_value(self.speed, MAX_SPEED)),
            "rpm": self.rpm_to_vol(self.normalize_value(self.rpm, self.max_rpm)),
            "pedal": self.pedal_to_vol(self.pedal) # This won't really get used
        }