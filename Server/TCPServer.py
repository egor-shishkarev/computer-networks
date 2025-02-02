import socket

HOST = "192.168.0.106"
PORT = 30000
data_payload = 2048
backlog = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("Starting up echo server on %s port %s" % (HOST, PORT))
sock.bind((HOST, PORT))

sock.listen(backlog)

while True:
    print("Waiting to receive message from client")
    client, address = sock.accept()
    print("Client connected from %s" % (address,))
    data = client.recv(data_payload)
    if data:
        print("Data: %s" % data)
        s = client.send(data)
        print("sent %s bytes back" % (s,))
    # end connection
    client.close()
