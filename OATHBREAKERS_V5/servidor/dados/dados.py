import threading
import json
from typing import Dict, Tuple

class Dados:
    def __init__(self):
        self.jogadores = []
        self.messages = []
        self.players_fight = []
        self.nr_jogadores = 0
        self.classes = {}
        self.itens = {}
        self.inimigos = {}
        self.lock = threading.Lock()

        with open("servidor/dados/classes.json","r",encoding="utf-8") as f:
            self.classes = json.load(f)
        with open("servidor/dados/itens.json", "r", encoding="utf-8") as f:
            self.itens = json.load(f)
        with open("servidor/dados/inimigos.json", "r", encoding="utf-8") as f:
            self.inimigos = json.load(f)

    def registar_player(self, player: dict):
        with self.lock:
            if player not in self.jogadores:
                self.jogadores.append(player)
                self.nr_jogadores += 1

    def remover_player(self, address):
        with self.lock:
            self.jogadores = [p for p in self.jogadores if p["jogador"] != address]
            self.nr_jogadores = len(self.jogadores)
    
    def atualizar_player(self, address, new_info: dict):
        with self.lock:
            for p in self.jogadores:
                if p["jogador"] == address:
                    p.update(new_info)
                    break

    def get_players_info(self, players=None):
        with self.lock:
            if players is None:
                return [
                    {k: v for k, v in p.items() if k != "conexao"}
                    for p in self.jogadores
                ]
            else:
                return [
                    {k: v for k, v in p.items() if k != "conexao"}
                    for p in self.jogadores if p["nome"] in players
                ]
            
    def get_nr_clientes(self) -> int:
        return self.nr_jogadores
    
    def obter_destinos_udp(self) -> Dict[Tuple[str, int], Tuple[str, int]]:
        with self.lock:
            return {
                (p["jogador"][0], p["jogador"][1]): (p["jogador"][0], p["udp_port"])
                for p in self.jogadores
            }   
    
    def add_message(self, message: str):
        with self.lock:
            self.messages.append(message)
    
    def remove_message(self):
        with self.lock:
            self.messages.clear()
    
    def get_messages(self):
        with self.lock:
            return self.messages