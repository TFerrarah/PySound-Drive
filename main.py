import os
import time
import json
from numpy import average
from AudioStreams import AudioStreams
from OBDHandler import OBDHandler

DEBUG = False

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

#   Create JSON if not present
if not os.path.exists("car_ranges.json"):
    with open("car_ranges.json", "w") as json_file:
        json_file.write(json.dumps(json_base))

handler = OBDHandler()

with open("car_ranges.json", "r+") as json_file:
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

loop = AudioStreams(audio_components) # ! THIS IS WHERE AUDIO STARTS PLAYING

print(loop.get_streams_ports())

# Divide streams info
bass_port = loop.get_streams_ports()["Bass"]
drums_port = loop.get_streams_ports()["Drums"]
other_port = loop.get_streams_ports()["Other"]
vocals_port = loop.get_streams_ports()["Vocals"]

try:
    while True:
        time.sleep(0.01) # The less this value, the more accurate and responsive the audio change will be.

        # Get new values
        handler.refresh_values()

        # Get new volume and frequency values
        frequencies = handler.get_frequencies()
        volumes = handler.get_volumes()

        # calculate lpf frequency
        bass_freq = average([frequencies["pedal"], frequencies["rpm"]], weights=[.5, 1])
        drums_freq = average([frequencies["pedal"], frequencies["rpm"], frequencies["speed"]], weights=[.2, .2, 1])
        other_freq = average([frequencies["pedal"], frequencies["rpm"], frequencies["speed"]], weights=[.2, .2, 1])
        vocals_freq = average([frequencies["speed"]], weights=[1])

        # Calculate volumes
        bass_vol = average([volumes["pedal"], volumes["rpm"]], weights=[.5, 1])
        other_vol = average([volumes["pedal"], volumes["rpm"], volumes["speed"]], weights=[.4, 1, .2])
        drums_vol = average([volumes["speed"]], weights=[1])
        vocals_vol = average([volumes["speed"]], weights=[1])
        
        if DEBUG == True:
            print("FREQUENCIES ↓")
            print([bass_freq, drums_freq, other_freq, vocals_freq])
            print("VOLUMES ↓")
            print([bass_vol, drums_vol, other_vol, vocals_vol])
            print("RAW VOLUMES ↓")
            print(volumes)

            print("RAW FREQUENCIES ↓")
            print(frequencies)

            print("RAW PERCENTAGES ↓")
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

