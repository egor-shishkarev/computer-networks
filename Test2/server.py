import socket
import time
import random

# Определяем широковещательный адрес
BROADCAST_IP = "192.168.0.255"  # Для сети 192.168.0.x широковещательный адрес - 192.168.0.255
LOCAL_IP = "192.168.0.106"      # Ваш IP-адрес
MESSAGE = "Hello, this is broadcast message!"

# Создаем UDP-сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

try:
    while True:
        # Случайный порт в диапазоне 10000-60000
        random_port = random.randint(10000, 60000)
        
        # Отправляем сообщение
        sock.sendto(MESSAGE.encode("utf-8"), (BROADCAST_IP, random_port))
        print(f"Сообщение отправлено на {BROADCAST_IP}:{random_port}")
        
        # Ждем 2 секунды
        time.sleep(2)
finally:
    sock.close()
