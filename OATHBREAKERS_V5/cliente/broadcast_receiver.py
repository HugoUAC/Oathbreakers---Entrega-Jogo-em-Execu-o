import threading
import json
import os
import time

class BroadcastReceiver(threading.Thread):
    def __init__(self, udp_socket):
        super().__init__(daemon=True)
        self.udp_socket = udp_socket

    def receive_int(self, n_bytes: int) -> int:
        data = self.udp_socket.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def receive_object(self):
        data, addr = self.udp_socket.recvfrom(65536)
        obj = json.loads(data.decode('utf-8'))
        return obj, addr
    
    def exibir_mapa(self,mapa,largura):
        """Exibe o mapa no terminal"""
        # Exibe numeração das colunas
        print("  ", end="")
        for c in range(largura):
            print(f"{c} ", end="")
        print()
        
        # Exibe cada linha com sua numeração
        for i, linha in enumerate(mapa):
            print(f"{i} ", end="")
            for celula in linha:
                print(f"{celula} ", end="")
            print()

    def run(self):
        print("Receiver de broadcasts UDP ativa...")
        while True:
            try:
                players, addr = self.receive_object()
                os.system('cls')

                mapa_largura = players.pop()
                mapa = players.pop()
                self.exibir_mapa(mapa,mapa_largura)

                message = players.pop()

                #self.exibir_mapa(mapa)
                print("\n--- Broadcast do servidor ---")
                for p in players:
                    print(f"  {p['nome']} | Classe: {p['classe']} | Status: {p['status']} | HP: {p['vida']} | MP: {p['mana']}")
                print("-----------------------------")
                print("")
                print(f"---SERVER MESSAGES---")  # Exibe as mensagens recebidas
                for msg in message:
                    print(f"  {msg}")
                print("-------------------")
            except Exception as e:
                print(f"Receiver desconectado: {e}")
                break
