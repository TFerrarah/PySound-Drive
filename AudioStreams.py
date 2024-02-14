import os
import subprocess
import zmq

## Audio stream

STARTING_LPF = 200
INITIAL_ZMQ_PORT = 5560
STARTING_VOLUME = 0

def create_audio_cmd(audio, port):
    return "ffplay -ss 160 -loop 0 -hide_banner -loglevel error -nodisp -af \"lowpass@lpf="+str(STARTING_LPF)+",volume@vol="+str(STARTING_VOLUME)+",azmq=bind_address=tcp\\\\\\://127.0.0.1\\\\\\:"+str(port)+"\" \""+audio+"\""

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
        
        self.streams=self.streams[:-3] # Remove last separator from streams
        # Start all streams
        self.ffplay_process = subprocess.Popen(self.streams, shell=True)

        # Start zmq sockets
        self.context = zmq.Context()
        # set context timeout
        self.context.setsockopt(zmq.RCVTIMEO, 1000)

        # self.sockets = {}
        # for p in self.streams_ports.values():
        #     self.sockets[str(p)] = self.context.socket(zmq.REQ)
        #     self.sockets[str(p)].connect("tcp://127.0.0.1:"+str(p))

    def get_streams_ports(self):
        return self.streams_ports

    # This was the optimal solution, however it does not go well with ffplay's problems with looping and zmq
    # def change_lpf(self, frequency, port):
    #     self.sockets[str(port)].send_string("lowpass@lpf frequency "+str(frequency))
    #     self.sockets[str(port)].recv()
    
    # def change_vol(self, volume ,port):
    #     self.sockets[str(port)].send_string("volume@vol volume "+str(volume))
    #     self.sockets[str(port)].recv()

    def change_lpf(self,frequency,port):
        # Create new socket
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://127.0.0.1:"+str(port))
        # Send lpf change
        try:
            socket.send_string("lowpass@lpf frequency "+str(frequency))
            socket.recv()
        except Exception as e:
            print("[LPF - "+str(port)+" ] Delay on frequency change detected: "+str(e))
        finally:
            socket.close()
    
    def change_vol(self,volume,port):
        # Create new socket
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://127.0.0.1:"+str(port))
        # Send volume change
        try:
            socket.send_string("volume@vol volume "+str(volume))
            socket.recv()
        except Exception as e:
            print("[VOL - "+str(port)+" ] Delay on volume change response detected: "+str(e))
        finally:
            socket.close()

    def stop_streams(self):
        self.context.term()
        self.ffplay_process.terminate()