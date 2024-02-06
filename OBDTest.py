import zmq

ZMQ_IP = "tcp://127.0.0.1:5560"

# Subscribe to PUB/SUB server on 127.0.0.1:5560
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(ZMQ_IP)

# Send message to server
socket.send_string("volume@vol volume 0")

# Close connection
socket.close()