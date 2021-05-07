import socket, threading
from threading import Thread

from consts import *

blackboard = [[(0, 0, 0) for j in range(WINDOW_SIZE[0])] for i in range(WINDOW_SIZE[1])]

clients = set()
clients_lock = threading.Lock()

def handle_client(client):
    with clients_lock:
        clients.add(client)
    for i in range(len(blackboard)):
        for j in range(len(blackboard[i])):
            px = Pixel((j,i),blackboard[i][j])
            client.send(px.tostring().encode())
    try:
        while True:
            data = client.recv(BUFSIZE)
            if not data:
                break

            r=data.decode().split('.')[:-1]
            for i in r:
                pixel = Pixel()
                pixel.fromstring(i)
                blackboard[pixel.position[0]][pixel.position[1]] = pixel.color
            with clients_lock:
                for c in clients:
                    if (c != client):
                        c.sendall(data)
    except:
        print('c pa bien')
    with clients_lock:
        clients.remove(client)
        client.close()


sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))

sock.listen()

print(f"Server is listening on {PORT}")
while True:
    client, adress = sock.accept()
    Thread(target = handle_client, args = (client, )).start()