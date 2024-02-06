import zmq
import math
import time

ZMQ_IP = "tcp://127.0.0.1:5560"

# Subscribe to PUB/SUB server on 127.0.0.1:5560
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(ZMQ_IP)

# # Send message to server
# socket.send_string("volume@vol volume 0")

# # Close connection
# socket.close()

# Adjust volume and frequency 90 times per second (90Hz refresh rate)

while True:
    time.sleep(1/90)

    # Volume should follow a sinusoidal pattern from 0 to 1
    vol = (math.sin(time.time())+1)/2

    # frequency should follow a sinusoidal pattern from 200 to 20000
    freq = 200 + 19800*(math.sin(time.time())+1)/2

    print("Sending...")
    # send message to server
    # socket.send_string("volume@vol volume "+str(vol))
    socket.send_string("lowpass@lpf frequency "+str(freq))
    # get server response
    message = socket.recv()
    print("Received reply: ", message)

# Start multiple audio streams and set their volume and frequency
    
