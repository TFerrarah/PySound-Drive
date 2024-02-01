import os
import platform
import time
import subprocess

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

        for c in components:
            filename = os.path.splitext(os.path.basename(c))[0]
            print(filename +" -> "+ str(port))
            self.streams.append(subprocess.Popen(create_audio_cmd(c, port), shell=True))
            self.streams_ports[filename] = port
            port = port+1
    
    def get_streams_ports(self):
        return self.streams_ports

    def change_lpf(self, frequency, port):
        cmd_lpf = "echo lowpass@lpf frequency "+str(frequency)+" | zmqsend -b tcp://127.0.0.1:"+str(port)
        subprocess.run(cmd_lpf, shell=True, stdout = subprocess.DEVNULL)
    
    def change_vol(self, volume ,port):
        cmd_vol = "echo volume@vol volume "+str(volume)+" | zmqsend -b tcp://127.0.0.1:"+str(port)
        subprocess.run(cmd_vol, shell=True, stdout = subprocess.DEVNULL)

    def stop_streams(self):
        for s in self.streams:
            s.terminate()


# ! Working
# cmd = "ffplay -ss 14 -hide_banner -loglevel error -showmode 0 -loop 0 -af 'lowpass@lpf=20000,azmq' "+cwd+original
# p = subprocess.Popen(cmd, shell=True)
# time.sleep(5)
# enable_lpf = "echo lowpass@lpf frequency 200 | zmqsend"
# subprocess.run(enable_lpf, shell=True,stdout=open(os.devnull, 'wb'))
# time.sleep(5)
# p.terminate()