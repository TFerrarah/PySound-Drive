import os
import subprocess

VERBOSE = False

# Install yt-dlp if not already installed
cmd = """
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o ~/.local/bin/yt-dlp
chmod a+rx ~/.local/bin/yt-dlp  # Make executable
"""

if not os.path.exists("~/.local/bin/yt-dlp"):
    if VERBOSE: print("Installing yt-dlp...")
    subprocess.run(cmd, shell=True)

# USER INPUT
# TODO Remove the need for user input

# request songs from youtube playlist and fetch timestamps for each song from playlist description using yt-dlp



song = input("Enter the song name: ")