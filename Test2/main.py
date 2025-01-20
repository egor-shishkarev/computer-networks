# import socket
# from scapy.all import UDP, IP, sniff
# import re


# def packet_callback(pkt):
#     try:
#         if pkt.haslayer(UDP):
#             if pkt[IP] and pkt[IP].dst == "192.168.0.255":
#                 if pkt.haslayer("Raw"):
#                     print(f"Получен пакет от {pkt[IP].src} на порт {pkt[UDP].sport} -> {pkt[UDP].dport}")
#                     print(pkt.show())
#                     load = pkt["Raw"].load.decode('utf-8', errors='ignore')
#                     print(f"Загруженные данные: {load}")
#                     match = re.search(r"port = (\d+)", load)
#                     if match:
#                         port = int(match.group(1))
#                         print(f"Попытка подключиться к 192.168.1.108 на порт {port}...")
#                         try:
#                             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                                 s.connect(("192.168.1.108", port))
#                                 print(f"Подключено к 192.168.1.108:{port}")
#                                 response = s.recv(1024)
#                                 print(f"Получено сообщение: {response.decode('utf-8')}")
#                         except Exception as e:
#                             print(f"Ошибка при подключении: {e}")
#     except IndexError:
#         print("Ошибка: слой IP не найден. Пропускаем пакет и продолжаем.")
#         pass

# sniff(prn=packet_callback, filter="udp", store=0) 


import socket
from scapy.all import UDP, IP, sniff
import re


def packet_callback(pkt):
    try:
        if pkt.haslayer(UDP):
            if pkt[IP] and pkt[IP].dst == "192.168.0.255":
                if pkt.haslayer("Raw"):
                    print(f"Получен пакет от {pkt[IP].src} на порт {pkt[UDP].sport} -> {pkt[UDP].dport}")
                    print(pkt.show())
                    load = pkt["Raw"].load.decode('utf-8', errors='ignore')
                    print(f"Загруженные данные: {load}")
                    match = re.search(r"port = (\d+)", load)
                    if match:
                        port = int(match.group(1))
                        print(f"Попытка подключиться к 192.168.1.108 на порт {port}...")
                        try:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                s.connect(("192.168.1.108", port))
                                print(f"Подключено к 192.168.1.108:{port}")
                                response = s.recv(1024)
                                print(f"Получено сообщение: {response.decode('utf-8')}")
                        except Exception as e:
                            print(f"Ошибка при подключении: {e}")
    except IndexError:
        print("Ошибка: слой IP не найден. Пропускаем пакет и продолжаем.")
        pass

sniff(prn=packet_callback, filter="udp", store=0)
