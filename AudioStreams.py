import os
import subprocess
import zmq

## Audio stream

STARTING_LPF = 200
INITIAL_ZMQ_PORT = 5560
STARTING_VOLUME = 0

def create_audio_cmd(audio, port):
    return "ffplay -hide_banner -loglevel error -nodisp -loop 0 -af \"lowpass@lpf="+str(STARTING_LPF)+",volume@vol="+str(STARTING_VOLUME)+",azmq=bind_address=tcp\\\\\\://127.0.0.1\\\\\\:"+str(port)+"\" "+audio

class AudioStreams():

    def __init__(self, components) -> None:
        # Start audio streams
        self.streams = ""
        self.streams_ports = {}
        port = INITIAL_ZMQ_PORT

        for c in components:
            filename = os.path.splitext(os.path.basename(c))[0]
            print(filename +" -> "+ str(port))
            # self.streams.append(subprocess.Popen(create_audio_cmd(c, port), shell=True))
            self.streams += create_audio_cmd(c, port) + " | "
            self.streams_ports[filename] = port
            port = port+1
        
        streams=streams[:-3] # Remove last separator from streams
        # Start all streams
        self.ffplay_process = subprocess.Popen(streams, shell=True)

        # Start zmq sockets
        self.context = zmq.Context()

        self.sockets = {}
        for p in self.streams_ports.values():
            self.sockets[str(p)] = self.context.socket(zmq.REQ)
            self.sockets[str(p)].connect("tcp://127.0.0.1:"+str(p))

    def get_streams_ports(self):
        return self.streams_ports

    def change_lpf(self, frequency, port):
        self.sockets[str(port)].send_string("lowpass@lpf frequency "+str(frequency))
        self.sockets[str(port)].recv()
    
    def change_vol(self, volume ,port):
        self.sockets[str(port)].send_string("volume@vol volume "+str(volume))
        self.sockets[str(port)].recv()

    def stop_streams(self):
        self.ffplay_process.terminate()