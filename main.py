#!/usr/local/bin/python3

import obd
import os
import time
import subprocess
from AudioStreams import AudioStreams


# Audio Stuff
cwd = os.getcwd();
separated_audio_dir = cwd+"/Audio/Separated/"
AUDIO_EXT = [".mp3", ".m4a", ".flac", ".wav"] # You can add more audio extensions here, as long as they are supported in ffplay

# Get audio files
# TODO: Remove original song
original_song = cwd+"/Audio/Original.mp3"

# List of absolute paths for the component of the song
# This is done to ensure future-proofing to enable variations of other audio channels
# Only Bass, Drums, Vocals and "Other" channels will be used
audio_components = [separated_audio_dir+file for file in os.listdir(separated_audio_dir) if file.endswith(tuple(AUDIO_EXT))]

loop = AudioStreams(audio_components) # ! THIS IS WHERE AUDIO STARTS PLAYING

try:
    while True:
        time.sleep(0.05) # The less this value, the more accurate and responsive the audio change will be.

except KeyboardInterrupt:
    loop.stop_streams()
    print("\nGoodbye!")

loop.stop_streams()

