import time

import servidor
import json
import threading
from servidor.operacoes.movimento import Movimento
from servidor.operacoes.luta import Luta

class ProcessaCliente(threading.Thread):
    def __init__(self, connection, address, dados, mapa):
        super().__init__()
        self.connection = connection
        self.address = address
        self.dados = dados
        self.mapa = mapa
        self.mov = Movimento(connection, address,self.mapa,self)
        self.udp_port = None

    #----------interaction with sockets ---------------
    def receive_int(self,connection, n_bytes: int) -> int:
        data = connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_int(self,connection, value: int, n_bytes: int) -> None:
        connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_str(self,connection, n_bytes: int) -> str:
        data = connection.recv(n_bytes)
        return data.decode()

    def send_str(self,connection, value: str) -> None:
        connection.sendall(value.encode())

    def send_object(self,connection, obj):
        """1º: envia tamanho, 2º: envia dados."""
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(connection, size, servidor.INT_SIZE)
        connection.send(data)

    def receive_object(self,connection):
        """1º: lê tamanho, 2º: lê dados."""
        size = self.receive_int(connection, servidor.INT_SIZE)
        data = connection.recv(size)
        return json.loads(data.decode('utf-8'))
    
    def start_fight(self,player):

        self.send_int(self.connection, len(self.dados.players_fight),servidor.INT_SIZE)

        if len(self.dados.players_fight) == 0:
            choice = self.receive_str(self.connection, servidor.COMMAND_SIZE)
            if choice == servidor.WAIT_OP:
                self.dados.players_fight.append(player)
                self.dados.add_message(f"{player['nome']} está à espera do companheiro para atacar o inimigo.")
                time.sleep(30)
                if len(self.dados.players_fight) == 2:
                    luta = Luta(self.connection, self.address, self.dados)
                    self.dados.remove_message()
                    return luta.luta(self.dados.players_fight[0], self.dados.players_fight[1])

                else:
                    luta = Luta(self.connection, self.address, self.dados)
                    self.dados.remove_message()
                    return luta.luta(self.dados.players_fight[0])

            elif choice == servidor.ATTACK_OP:
                luta = Luta(self.connection, self.address, self.dados)
                for p in self.dados.get_players_info():
                    if p["jogador"] == self.address:
                        return luta.luta(p)
            else:
                print(f"Opção de luta inválida recebida de {self.address}: {choice}")
        else:
            self.dados.players_fight.append(player)
            return False
    #--------

    def run(self):
        print(self.address, "Thread iniciada")
        self.udp_port = self.receive_int(self.connection, servidor.INT_SIZE)
        print(f"[{self.address}] Porta UDP recebida: {self.udp_port}")

        name = self.receive_str(self.connection, servidor.COMMAND_SIZE)

        self.send_object(self.connection, self.dados.classes)
        classe = self.receive_object(self.connection)

        player = {
            "jogador": self.address,
            "conexao": self.connection,
            "udp_port": self.udp_port,
            "nome": name.strip(),
            "posicao": [0,0],
            "classe": classe["nome"],
            "nivel": 0,
            "ouro": 0,
            "experiencia": 0,
            "vida": classe["vida"],
            "mana": classe["mana"],
            "inventario": [],
            "status": "vasculhando"
        }
        self.dados.registar_player(player)
        
        if self.mapa.obter_elemento(1,1) == servidor.EMPTY:
            self.mapa.adicionar_elemento(1,1,player["nome"][0])
            player["posicao"] = [1,1]
        else:
            self.mapa.adicionar_elemento(2,1,player["nome"][0])
            player["posicao"] = [2,1]

        last_request = False
        while not last_request:
            self.send_str(self.connection,servidor.EMPTY)
            request_type = self.receive_str(self.connection, servidor.COMMAND_SIZE)

            if request_type == servidor.MOVE_UP:
                self.mov.move_up(player)

            elif request_type == servidor.MOVE_DOWN:
                self.mov.move_down(player)

            elif request_type == servidor.MOVE_LEFT:
                self.mov.move_left(player)

            elif request_type == servidor.MOVE_RIGHT:
                self.mov.move_right(player)

            elif request_type == servidor.HEAL_OP:
                player = self.dados.get_players_info(player["nome"])[0]
                for classe in self.dados.classes:
                    if classe["nome"] == player["classe"]:
                        classe_player = classe
                        break
                vida = player["vida"] 

                if vida + 50 >= classe_player["vida"]:
                    self.dados.atualizar_player(self.connection,{"vida":classe_player["vida"]})
                else:
                    self.dados.atualizar_player(self.connection,{"vida":vida+50})

            elif request_type == servidor.BYE_OP:
                last_request = True
                self.dados.remover_player(self.address)
                print(self.address, "Thread terminada")
                self.connection.close()
            elif request_type == servidor.END_OP:
                pass
