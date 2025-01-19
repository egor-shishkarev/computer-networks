import socket
import select

HOST = "localhost"
PORT = 5555
data_payload = 2048

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((HOST, PORT))

while True:
    print("Waiting to receive message from client")
    data, address = sock.recvfrom(data_payload)
    print(address)
    if address[0] != '8.8.8.8':
        print('Получено сообщение из неизвестного источника.')
        sock.sendto(b'You have not rights to perform operation!', address)
        continue

    if not data:
        continue

    print("Received %s bytes from %s" % (len(data), address))
    print(f'Полученные данные - {data}')
    ip_address, port = str(data)[2:-1].split(':')
    print(f'IP_ADDRESS = {ip_address}, PORT = {port}')
    try:
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect((ip_address, int(port)))

        print(f'Установлено соединение с {ip_address}:{port}')

        tcp_sock.send(b'GET / HTTP/1.1\nHost: 1.1.1.1\nConnection: close\n\n')

        rdy = select.select([tcp_sock], [], [], 10)
        if not rdy[0]:
            raise RuntimeError("no response")

        data = tcp_sock.recv(4096)

        if not data:
            raise RuntimeError("socket connection broken")

        print(data)
    except Exception as e:
        print(f'Возникла ошибка - {e}')

