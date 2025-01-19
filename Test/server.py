import socket

HOST = "localhost"
PORT = 5555
data_payload = 2048

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((HOST, PORT))

while True:
    print("Waiting to receive message from client")
    data, address = sock.recvfrom(data_payload)
    print(address)
    if address != '8.8.8.8':
        print('Получено сообщение из неизвестного источника.')
        sock.sendto(b'You have not rights to perform operation!', address)
        continue

    if not data:
        continue

    print("Received %s bytes from %s" % (len(data), address))
    s = sock.sendto(data, address)
    print("Sent %s bytes back" % (s,))