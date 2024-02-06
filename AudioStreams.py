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
        self.streams = []
        self.streams_ports = {}
        port = INITIAL_ZMQ_PORT

        for c in components:
            filename = os.path.splitext(os.path.basename(c))[0]
            print(filename +" -> "+ str(port))
            self.streams.append(subprocess.Popen(create_audio_cmd(c, port), shell=True))
            self.streams_ports[filename] = port
            port = port+1

        # Start zmq sockets
        self.context = zmq.Context()

        self.sockets = {}
        for p in self.streams_ports.values():
            self.sockets[str(p)] = self.context.socket(zmq.REQ)
            self.sockets[str(p)].connect("tcp://127.0.0.1:"+str(p))


    
    def get_streams_ports(self):
        return self.streams_ports

    def change_lpf(self, frequency, port):
        # cmd_lpf = "echo lowpass@lpf frequency "+str(frequency)+" | zmqsend -b tcp://127.0.0.1:"+str(port)
        # subprocess.run(cmd_lpf, shell=True, stdout = subprocess.DEVNULL)
        self.sockets[str(port)].send_string("lowpass@lpf frequency "+str(frequency))
    
    def change_vol(self, volume ,port):
        # cmd_vol = "echo volume@vol volume "+str(volume)+" | zmqsend -b tcp://127.0.0.1:"+str(port)
        # subprocess.run(cmd_vol, shell=True, stdout = subprocess.DEVNULL)
        self.sockets[str(port)].send_string("volume@vol volume "+str(volume))

    def stop_streams(self):
        for s in self.streams:
            s.terminate()