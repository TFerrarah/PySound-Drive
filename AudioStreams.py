import os
import time
import subprocess
import zmq

## Audio stream

STARTING_LPF = 200
INITIAL_ZMQ_PORT = 5560
STARTING_VOLUME = 0

def create_audio_cmd(audio, port):
    return "ffplay -ss 14 -hide_banner -loglevel error -nodisp -loop 0 -af 'lowpass@lpf="+str(STARTING_LPF)+",volume@vol="+str(STARTING_VOLUME)+",azmq=bind_address=tcp\\\\\\://127.0.0.1\\\\\\:"+str(port)+"' "+audio

class AudioStreams():

    def __init__(self, components) -> None:
        # Start audio streams
        self.streams = []
        self.streams_ports = {}
        port = INITIAL_ZMQ_PORT
        self.zmq_sockets = {}
        context = zmq.Context()

        for c in components:
            filename = os.path.splitext(os.path.basename(c))[0]
            print(filename +" -> "+ str(port))
            self.streams.append(subprocess.Popen(create_audio_cmd(c, port), shell=True))
            self.streams_ports[filename] = port
            # Start zmq_sockets
            self.zmq_sockets[str(port)] = context.socket(zmq.PUB)
            print("socket created")
            self.zmq_sockets[str(port)].bind('tcp://*:'+str(port))
            print("socket connected")
            port = port+1

    
    def get_streams_ports(self):
        return self.streams_ports

    def change_lpf(self, frequency, port):
        cmd_lpf = "echo lowpass@lpf frequency "+str(frequency)+" | zmqsend -b tcp://127.0.0.1:"+str(port)
        subprocess.run(cmd_lpf, shell=True, stdout = subprocess.DEVNULL)
        # self.socket.send("%s %s" % ("554", "echo lowpass@lpf frequency "+str(frequency)))
    
    def change_vol(self, volume ,port):
        cmd_vol = "echo volume@vol volume "+str(volume)+" | zmqsend -b tcp://127.0.0.1:"+str(port)
        subprocess.run(cmd_vol, shell=True, stdout = subprocess.DEVNULL)
        # self.socket.send("%s %s" % ("554", "echo volume@vol volume "+str(volume)))

    def stop_streams(self):
        for s in self.streams:
            s.terminate()