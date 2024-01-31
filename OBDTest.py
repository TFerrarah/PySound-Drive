import os
import json

json_base = {"pedal" : [-1,-1],"redline" : -1,"idle" : -1}

#   Create JSON if not present
if not os.path.exists("car_ranges.json"):
    with open("car_ranges.json", "w") as json_file:
        json_file.write(json.dumps(json_base))

with open("car_ranges.json", "r+") as json_file:
    car_values = json.load(json_file)

    # Here you can edit car_values attributes


    # Write to file
    json_file.seek(0)
    json_file.write(json.dumps(car_values))
    json_file.truncate()

# Read file
with open("car_ranges.json", "r") as json_file:
    car_values = json.load(json_file)
    
    # Do stuff with car_values