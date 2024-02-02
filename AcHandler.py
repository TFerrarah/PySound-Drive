from pyaccsharedmemory import accSharedMemory
import math
import json

MAX_SPEED = 150

class AcHandler():
    def __init__(self):

        # Initiate assetto corsa Shared memory reader

        self.asm = accSharedMemory()

        # Reset values
        self.speed = 0
        self.rpm = 0
        self.pedal = 0

        # Read values from JSON file
        with open("car_ranges.json", "r") as json_file:
            car_values = json.load(json_file)
            self.redline = car_values["redline"]
            self.idle = car_values["idle"]

    def refresh_values(self): 
        sm = self.asm.read_shared_memory() # Read AC shared memory
        self.speed = sm.Physics.speed_kmh
        self.rpm = sm.Physics.rpm
        self.pedal = sm.Physics.gas
    
    # Get raw values
    def get_speed(self):
        return self.speed
    def get_rpm(self):
        return self.rpm
    def get_pedal(self):
        return self.pedal
    
    # Value to frequency conversion formulas

    def pedal_to_freq(self, percentage):
        r= 20000 * percentage + 3 # Formula calculated using https://www.dcode.fr/function-equation-finder
        if r < 200 : r = 200 
        elif r > 20000 : r = 20000
        return r
    
    def rpm_to_freq(self, percentage):
        r= 68241*percentage-13525.3 # Formula calculated using https://www.dcode.fr/function-equation-finder
        if r < 200 : r = 200 
        elif r > 20000 : r = 20000
        return r
    
    def speed_to_freq(self, percentage):
        r=1874.42*math.log(2079.27*percentage+0.0331104)+6587.76 # Formula calculated using https://www.dcode.fr/function-equation-finder
        if r < 200 : r = 200 
        elif r > 20000 : r = 20000
        return r
    
    # Value to volume conversion formulas

    def speed_to_vol(self, raw_speed):
        if raw_speed <= 40: r = 0.000940424*raw_speed**2-0.00357231*raw_speed -0.0102372 
        else: r = 1

        if r < 0 : r = 0 
        elif r > 1 : r = 1
        return r

    def rpm_to_vol(self, percentage):
        r = 2 * percentage
        if r < 0 : r = 0 
        elif r > 1 : r = 1
        return percentage + .2 # Idle rpm volume is too low, so we add a constant value to it
    
    # Utility functions

    def normalize_value(self, curr, min_value, max_value):
        normalized_value = (curr - min_value) / (max_value - min_value)
        return normalized_value
    
    # No calibration is needed since value is already in percentage

    def get_percentages(self):
        return {
            "speed": self.normalize_value(self.speed, 0 , MAX_SPEED), # Speed_normalized = 2/300 * real speed
            "rpm": self.normalize_value(self.rpm, self.idle , self.redline),
            "pedal": self.pedal
        }
    
    def get_frequencies(self):
        return {
            "speed": self.speed_to_freq(self.normalize_value(self.speed, 0 , MAX_SPEED)),
            "rpm": self.rpm_to_freq(self.normalize_value(self.rpm, self.idle , self.redline)),
            "pedal": self.pedal_to_freq(self.pedal)
        }
    
    def get_volumes(self):
        return {
            "speed": self.speed_to_vol(self.speed),
            "rpm": self.rpm_to_vol(self.normalize_value(self.rpm, self.idle , self.redline)),
            "pedal": self.pedal # This value is already a percentage, thus it doens't need a special formula
        }