import subprocess
import os
import sys

AUDIO_EXT = [".mp3", ".m4a", ".flac", ".wav"] # You can add more audio extensions here, as long as they are supported in ffplay

port = 5560

cwd = os.getcwd();
separated_audio_dir = cwd+"/Audio/Separated/"

audio_components = [separated_audio_dir+file for file in os.listdir(separated_audio_dir) if file.endswith(tuple(AUDIO_EXT))]

def create_audio_cmd(audio, port):
    cmd = "ffplay -ss 14 -hide_banner -loglevel error -nodisp -loop 0 -af 'lowpass@lpf=200,volume@vol=0,azmq=bind_address=tcp\\\\\\://127.0.0.1\\\\\\:"+str(port)+"' "+audio
    print(cmd)
    return cmd

streams = []
streams_ports = {}

# for c in audio_components:
#             filename = os.path.splitext(os.path.basename(c))[0]
#             print(filename +" -> "+ str(port))
#             streams.append(subprocess.Popen(create_audio_cmd(c, port), shell=True))
#             streams_ports[filename] = port
#             port = port+1

print(streams_ports)

subprocess.Popen("ffplay -ss 14 -hide_banner -loglevel error -nodisp -loop 0 -af \"lowpass@lpf=200,volume@vol=0,azmq=bind_address=tcp\\\://127.0.0.1\\\:5563\" T:\Tommaso\Downloads\PySound-Drive-GH\PySound-Drive/Audio/Separated/Vocals.m4a", shell=True)
