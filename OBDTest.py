import zmq
import math
import time
import subprocess
import os

# Adjust volume and frequency 90 times per second (90Hz refresh rate)

# SINGLE = False

# while SINGLE:
#     time.sleep(1/90)

#     # Volume should follow a sinusoidal pattern from 0 to 1
#     vol = (math.sin(time.time())+1)/2

#     # frequency should follow a sinusoidal pattern from 200 to 20000
#     freq = 200 + 19800*(math.sin(time.time())+1)/2

#     print("Sending...")
#     # send message to server
#     # socket.send_string("volume@vol volume "+str(vol))
#     socket.send_string("lowpass@lpf frequency "+str(freq))
#     # get server response
#     message = socket.recv()
#     print("Received reply: ", message)

# Start multiple audio streams and set their volume and frequency
    
def create_audio_cmd(audio, port):
    return "ffplay -ss 14 -hide_banner -loglevel error -nodisp -loop 0 -af \"lowpass@lpf="+str(20000)+",volume@vol="+str(0)+",azmq=bind_address=tcp\\\\\\://127.0.0.1\\\\\\:"+str(port)+"\" "+audio

streams = []
streams_ports = {}
# For each file in ./Audio run subprocess.Popen(create_audio_cmd(c, port), shell=True) where port is 5560 + i
port = 5560
for audio in os.listdir("./Audio"):
    if audio.endswith(".m4a"):
        filename = os.path.splitext(os.path.basename(audio))[0]+".m4a"
        print(filename +" -> "+ str(port))
        streams.append(subprocess.Popen(create_audio_cmd("./Audio/"+audio, port), shell=True))
        streams_ports[filename] = port
        port = port+1

# Start zmq sockets and contexes for each port
contexes = {}
sockets = {}
for p in streams_ports.values():
    contexes[str(p)] = zmq.Context()
    sockets[str(p)] = contexes[str(p)].socket(zmq.REQ)
    sockets[str(p)].connect("tcp://127.0.0.1:"+str(p))

# Adjust volume and frequency 90 times per second on each stream with the same sinusoidal pattern, alternating on each stream (One should be sinusoidal, the other should be the inverse of the first one)
MULTI = True

while MULTI:
    time.sleep(1/90)
    for p in streams_ports.values():
        # Volume should follow a sinusoidal pattern from 0 to 1
        vol = (math.sin(time.time())+1)/2

        # frequency should follow a sinusoidal pattern from 200 to 20000
        freq = 200 + 19800*(math.sin(time.time())+1)/2

        # send message to server
        sockets[str(p)].send_string("volume@vol volume "+str(vol))
        # receive message [MANDATORY]
        sockets[str(p)].recv()
        sockets[str(p)].send_string("lowpass@lpf frequency "+str(freq))
        # receive message [MANDATORY]
        sockets[str(p)].recv()

# Stop all streams on exit
for s in streams:
    s.terminate()