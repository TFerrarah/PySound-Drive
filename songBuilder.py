import json
import subprocess
import argparse
import os
import shutil

# # Install yt-dlp if not already installed
# cmd = """
# curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o ~/.local/bin/yt-dlp
# chmod a+rx ~/.local/bin/yt-dlp  # Make executable
# """

# if not os.path.exists("~/.local/bin/yt-dlp"):
#     if VERBOSE: print("Installing yt-dlp...")
#     subprocess.run(cmd, shell=True)

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL9FAVP824Gr-bZYQp8o31dKJSCVID2lAB"
PLAYLIST_FILE = "./playlist.json"

# Initialize parser
parser = argparse.ArgumentParser()
# Wipe car_values
parser.add_argument("-u", "--Update", help = "Update playlist file", action="store_true")

args = parser.parse_args()

# Get playlist information if file does not exist or update is explicitly requested
if args.Update or not os.path.exists(PLAYLIST_FILE):
    print("Updating playlist file...")
    cmd = f"yt-dlp --skip-download -I0 --print playlist:description \"{PLAYLIST_URL}\""
    description = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
    description = json.loads(description)
    with open(PLAYLIST_FILE, "w") as f:
        json.dump(description, f, indent=4)
    print("Playlist file updated")

# For each video in playlist, download it and trim it to the timestamps specified in the playlist.json file
with open(PLAYLIST_FILE, "r") as f:
    playlist = json.load(f)

# Download using the -I X argument where X is a number from 1 to playlist length and save it to /Audio/[SONG_NAME]/Original.wav
# be sure to respect video index in playlist and index in playlist.json
# If audio folder is empty, create it and do the for loop
if not os.path.exists("./Audio"):
    os.mkdir("./Audio")

    for i, video in enumerate(playlist["entries"]):
        title = video["title"]
        start = video["start"]
        end = video["end"]
        print(f"Downloading {title}...")
        cmd = f"yt-dlp -f \"bestaudio\" --extract-audio --no-playlist --output \"./Audio/{title}/Original.%(ext)s\" -I {i+1} {PLAYLIST_URL}"
        subprocess.run(cmd, shell=True)

        # Trim the audio file to the specified timestamps
        print(f"Trimming {title}...")
        cmd = f"ffmpeg -n -i \"./Audio/{title}/Original.%(ext)s\" -ss {start} -to {end} -c copy \"./Audio/{title}/Trimmed.%(ext)s\""
        subprocess.run(cmd, shell=True)

        # Remove the original audio file
        os.remove(f"./Audio/{title}/Original.%(ext)s")


# Use facebook's demucs to separate the audio into vocals, drums, bass, and other
import demucs.separate
import shlex

# Separate audio and save to /Audio/[SONG_NAME]
os.chdir("./Audio")
for i, video in enumerate(playlist["entries"]):
    title = video["title"]
    print(f"Separating {title}...")
    # Change directory to song directory
    os.chdir(f"./{title}")
    # Separate audio
    MODEL = "htdemucs_ft"
    demucs.separate.main(shlex.split(f'-n {MODEL} -j 2 "./Trimmed.%(ext)s"'))
    # Move audio files from /separated/htdemucs to /Audio/[SONG_NAME]
    os.rename(f"./separated/{MODEL}/Trimmed/vocals.wav", "./Vocals.wav")
    os.rename(f"./separated/{MODEL}/Trimmed/drums.wav", "./Drums.wav")
    os.rename(f"./separated/{MODEL}/Trimmed/bass.wav", "./Bass.wav")
    os.rename(f"./separated/{MODEL}/Trimmed/other.wav", "./Other.wav")
    # Remove the separated directory
    shutil.rmtree("./separated")
    # Remove the trimmed audio file
    os.remove("./Trimmed.wav")
    # Return to root directory
    os.chdir("..")

print("Songs built successfully and ready to be used.")