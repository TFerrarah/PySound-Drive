import os
import time
import json
import argparse
from numpy import average
from AudioStreams import AudioStreams
from OBDHandler import OBDHandler
from AcHandler import AcHandler

DEBUG = False
VERBOSE = True

# Audio Stuff
cwd = os.getcwd();
separated_audio_dir = cwd+"/Audio/Separated/"
AUDIO_EXT = [".mp3", ".m4a", ".flac", ".wav"] # You can add more audio extensions here, as long as they are supported in ffplay

# TODO REMOVE ORIGINAL SONG
original_song = cwd+"/Audio/Original.mp3"

# List of absolute paths for the component of the song
# This is done to ensure future-proofing to enable variations of other audio channels
# Only Bass, Drums, Vocals and "Other" channels will be used
audio_components = [separated_audio_dir+file for file in os.listdir(separated_audio_dir) if file.endswith(tuple(AUDIO_EXT))]

# Manage car's values file
json_base = {"pedal" : [-1,-1],"redline" : -1,"idle" : -1}

CAR_INFO_FILENAME = "car_ranges.json"

#   Create JSON if not present
if not os.path.exists(CAR_INFO_FILENAME):
    with open(CAR_INFO_FILENAME, "w") as json_file:
        json_file.write(json.dumps(json_base))

# Initiate OBDHandler

# Initialize parser
parser = argparse.ArgumentParser()
# Adding source argument
parser.add_argument("-s", "--Source", help = "[OBD, AC (AssettoCorsa, ACC, OBDII and OBD2 are also valid)] Input data Source (Assetto Corsa Competizione also works)", default = "OBD")
# Wipe car_values
parser.add_argument("-w", "--Wipe", help = "Wipe calibration data", action="store_true")


# Read arguments from command line
args = parser.parse_args()

# Wipe car_values
if args.Wipe:
    with open(CAR_INFO_FILENAME, "w") as json_file:
        json_file.write(json.dumps(json_base))
    print("Calibration data wiped")
# Valid sources
VALID_SOURCES = ["OBD", "AssettoCorsa", "AC", "ACC", "OBDII", "OBD2"]
if args.Source in VALID_SOURCES:
    if args.Source in ["OBD", "OBDII", "OBD2"]:
        handler = OBDHandler()

        # Values Calibration
        with open(CAR_INFO_FILENAME, "r+") as json_file:
            car_values = json.load(json_file)
            if car_values["idle"] < 0 or car_values["redline"] < 0 or car_values["pedal"] == [-1,-1]:
                input("No PySound-Drive calibration data was found. Press ENTER when you're ready for PySound-Drive calibration...")
                # Calibrate idle rpm
                while True:
                    try:
                        car_values["idle"] = int(input("Please enter your car's idle RPM [e.g. 950, 1000]: "))
                        if 0 <= car_values["idle"] <= 15000:
                            break
                        else:
                            print("Idle RPM must be between 0 - 15000")
                    except ValueError:
                        print("Input not recognized. Try again")

                # Calibrate redline rpm
                while True:
                    try:
                        car_values["redline"] = int(input("Please enter your car's redline RPM [e.g. 4500, 8000]: "))
                        if 0 <= car_values["redline"] <= 15000:
                            break
                        else:
                            print("Redline RPM must be between 0 - 15000")
                    except ValueError:
                        print("Input not recognized. Try again")

                # Calibrate pedal
                car_values["pedal"] = handler.calibrate_pedal()

                # Write to file
                json_file.seek(0)
                json_file.write(json.dumps(car_values))
                json_file.truncate()

    elif args.Source in ["AssettoCorsa", "AC", "ACC"]:
        handler = AcHandler()

        # Assetto corsa calibration (No pedal)
        with open(CAR_INFO_FILENAME, "r+") as json_file:
            car_values = json.load(json_file)
            if car_values["idle"] < 0 or car_values["redline"] < 0:
                input("No PySound-Drive calibration data was found. Press ENTER when you're ready for PySound-Drive calibration...")
                # Calibrate idle rpm in ac

                print("Put your car in NEUTRAL and wait 3 seconds...")
                time.sleep(3)
                idle_values = []
                for i in range(1,5):
                    handler.refresh_values()
                    print("["+str(i)+"] Reading Idle RPM information...")
                    idle_values.append(handler.get_rpm())
                    time.sleep(0.5)

                car_values["idle"] = sum(idle_values) / len(idle_values)

                print("Idle RPM registered!")
                # Calibrate redline rpm
                input("Leave your car in NEUTRAL and REV to FULL GAS press ENTER when you're ready...")
                time.sleep(1)
                redline = []
                for i in range(1,5):
                    handler.refresh_values()
                    print("!KEEP PUSHING!")
                    print("["+str(i)+"] Reading Redline RPM information...")
                    redline.append(handler.get_rpm())
                    time.sleep(0.5)
                
                car_values["redline"] = sum(redline) / len(redline)


                # Write to file
                json_file.seek(0)
                json_file.write(json.dumps(car_values))
                json_file.truncate()
                print("Redline RPM registered!")

                print("✅ Calibration complete ✅")


    # Refresh values
    handler.refresh_calibrations()

else:
    print("Invalid source. Please use one of the following: "+str(VALID_SOURCES))
    exit()


input("Press ENTER to start Vibe Drive...")
loop = AudioStreams(audio_components) # ! THIS IS WHERE AUDIO STARTS PLAYING

print(loop.get_streams_ports())

# Divide streams info
bass_port = loop.get_streams_ports()["Bass"]
drums_port = loop.get_streams_ports()["Drums"]
other_port = loop.get_streams_ports()["Other"]
vocals_port = loop.get_streams_ports()["Vocals"]

try:
    while True:
        time.sleep(1/90) # The less this value, the more accurate and responsive the audio change will be.

        # Get new values
        handler.refresh_values()

        # Get new volume and frequency values
        frequencies = handler.get_frequencies()
        volumes = handler.get_volumes()

        # calculate lpf frequency
        if volumes["speed"] < 1: bass_freq = average([frequencies["pedal"], frequencies["rpm"]], weights=[.5, 1])
        else: bass_freq = frequencies["speed"]

        drums_freq = average([frequencies["pedal"], frequencies["rpm"], frequencies["speed"]], weights=[.2, .2, 1])
        other_freq = average([frequencies["pedal"], frequencies["rpm"], frequencies["speed"]], weights=[.2, .2, 1])

        vocals_freq = frequencies["speed"]

        # Calculate volumes
        if volumes["speed"] < 1: bass_vol = average([volumes["pedal"], volumes["rpm"]], weights=[.5, 1])
        else: bass_vol = volumes["speed"]

        other_vol = average([volumes["pedal"], volumes["rpm"], volumes["speed"]], weights=[.4, 1, .2])
        drums_vol = average([volumes["speed"]], weights=[1])
        
        vocals_vol = volumes["speed"]

        if VERBOSE:
            print("[RAW]    Speed =" + str(handler.get_speed()))
            print("[RAW]    RPM =" + str(handler.get_rpm()))
            print("[RAW]    Pedal =" + str(handler.get_pedal()))

        if DEBUG:
            print("[CALC]   FREQUENCIES ↓")
            print([bass_freq, drums_freq, other_freq, vocals_freq])
            print("[CALC]   VOLUMES ↓")
            print([bass_vol, drums_vol, other_vol, vocals_vol])

            print("[CALC]   RAW VOLUMES ↓")
            print(volumes)
            print("[CALC]   RAW FREQUENCIES ↓")
            print(frequencies)
            print("[CALC]   RAW PERCENTAGES ↓")
            print(handler.get_percentages())

        # Set Volumes
        loop.change_vol(bass_vol, bass_port)
        loop.change_vol(drums_vol, drums_port)
        loop.change_vol(other_vol, other_port)
        loop.change_vol(vocals_vol, vocals_port)

        # Set LPF frequency
        loop.change_lpf(bass_freq, bass_port)
        loop.change_lpf(drums_freq, drums_port)
        loop.change_lpf(other_freq, other_port)
        loop.change_lpf(vocals_freq, vocals_port)
        

except KeyboardInterrupt:
    loop.stop_streams()
    print("\nGoodbye!")

loop.stop_streams()

