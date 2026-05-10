# thread_broadcast.py
import socket
import servidor
import threading
import time
import json
from typing import Dict
from servidor.dados.dados import Dados

class ThreadBroadcast(threading.Thread):
    def __init__(self, mapa, dados: Dados, intervalo: int = 3):
        super().__init__(daemon=True)
        self.dados = dados
        self.intervalo = intervalo
        self.running = True
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mapa = mapa

    def send_int(self, connection, value: int, n_bytes: int) -> None:
        connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def send_object(self, connection, obj):
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(connection, size, servidor.INT_SIZE)
        connection.send(data)
    
    def send_object_udp(self, udp_address, obj):
        data = json.dumps(obj).encode('utf-8')
        self.udp_socket.sendto(data, udp_address)

    def broadcast_object(self, obj: Dict) -> None:
        destinos = self.dados.obter_destinos_udp()
        for address, udp_address in destinos.items():
            try:
                self.send_object_udp(udp_address, obj)
                print(f"Broadcast UDP enviado para {address} -> {udp_address}")
            except Exception as e:
                print(f"Erro ao enviar para {address}: {e}")

    def run(self):
        print("ThreadBroadcast ativa")
        while self.running:
            try:
                time.sleep(self.intervalo)
                broadcast = self.dados.get_players_info()
                broadcast.append(self.dados.get_messages())
                broadcast.append(self.mapa.mapa)
                broadcast.append(self.mapa.largura)
                self.broadcast_object(broadcast)
                print(f"Broadcast para {self.dados.get_nr_clientes()} clientes")
            except Exception as e:
                print(f"Erro: {e}")
                continue
        print("ThreadBroadcast terminada")
