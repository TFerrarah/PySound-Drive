import json
import subprocess
import argparse

VERBOSE = False

# # Install yt-dlp if not already installed
# cmd = """
# curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o ~/.local/bin/yt-dlp
# chmod a+rx ~/.local/bin/yt-dlp  # Make executable
# """

# if not os.path.exists("~/.local/bin/yt-dlp"):
#     if VERBOSE: print("Installing yt-dlp...")
#     subprocess.run(cmd, shell=True)

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL9FAVP824Gr-bZYQp8o31dKJSCVID2lAB"
print("Getting playlist info...")
# Get playlist description
cmd = f"yt-dlp --skip-download -I0 --print playlist:description \"{PLAYLIST_URL}\""
description = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")

# Decode description to get JSON and write to file
description = json.loads(description)
with open("playlist.json", "w") as f:
    json.dump(description, f, indent=4)

# Check for differences between local playlist file and remote playlist
# But only if the -u flag is passed

args = argparse.ArgumentParser()

if args.update:
    print("Checking for differences between local and remote playlist...")
    # Get playlist items
    cmd = f"yt-dlp --skip-download -J \"{PLAYLIST_URL}\""
    playlist = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
    playlist = json.loads(playlist)

    # Compare local and remote playlists
    with open("playlist.json", "r") as f:
        local_playlist = json.load(f)

    # Check for differences
    if playlist != local_playlist:
        print("Playlist has changed. Updating local playlist...")
        with open("playlist.json", "w") as f:
            json.dump(playlist, f, indent=4)
    else:
        print("Playlist has not changed.")