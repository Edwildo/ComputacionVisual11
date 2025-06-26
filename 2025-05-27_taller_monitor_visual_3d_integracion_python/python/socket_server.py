import socket, json
import socketio

sio = socketio.Client()
sio.connect('http://localhost:4000')   # servidor React

# Socket UDP receptor
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 10000))

while True:
    data, _ = sock.recvfrom(4096)
    d = json.loads(data.decode())
    print("Detectados:", d['detections'])
    sio.emit('data', d)
