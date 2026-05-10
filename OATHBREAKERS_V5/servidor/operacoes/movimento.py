import servidor
import time

class Movimento:
    def __init__(self, connection, address,mapa,PC):
        self.connection = connection
        self.address = address
        self.mapa = mapa
        self.PC = PC


    def move_up(self, player):
        linha_atual = player["posicao"][0]
        coluna_atual = player["posicao"][1]
        linha_nova = player["posicao"][0] - 1
        if self.mover_jogador(linha_atual,coluna_atual,linha_nova,coluna_atual,player):
            player["posicao"][0] -= 1

    def move_down(self, player):
        linha_atual = player["posicao"][0]
        coluna_atual = player["posicao"][1]
        linha_nova = player["posicao"][0] + 1
        if self.mover_jogador(linha_atual,coluna_atual,linha_nova,coluna_atual,player):
            player["posicao"][0] += 1

    def move_left(self, player):
        linha_atual = player["posicao"][0]
        coluna_atual = player["posicao"][1]
        coluna_nova = player["posicao"][1] - 1
        if self.mover_jogador(linha_atual,coluna_atual,linha_atual,coluna_nova,player):
            player["posicao"][1] -= 1

    def move_right(self, player):
        linha_atual = player["posicao"][0]
        coluna_atual = player["posicao"][1]
        coluna_nova = player["posicao"][1] + 1
        if self.mover_jogador(linha_atual,coluna_atual,linha_atual,coluna_nova,player):
            player["posicao"][1] += 1


    def mover_jogador(self, linha_atual, coluna_atual, nova_linha, nova_coluna,player):
        """Move um elemento de uma posição para outra"""
        if 0 <= nova_linha < self.mapa.altura and 0 <= nova_coluna < self.mapa.largura:

            if self.mapa.mapa[nova_linha][nova_coluna] == servidor.ENEMY:
                self.PC.send_str(self.PC.connection, servidor.ENEMY)
                time.sleep(1)
                
                if self.PC.start_fight(player):
                    elemento = self.mapa.mapa[linha_atual][coluna_atual]
                    self.mapa.mapa[linha_atual][coluna_atual] = servidor.EMPTY
                    self.mapa.mapa[nova_linha][nova_coluna] = elemento
                    return True

            elif self.mapa.mapa[nova_linha][nova_coluna] == servidor.CHEST:
                pass

            elif self.mapa.mapa[nova_linha][nova_coluna] == servidor.EMPTY:
                elemento = self.mapa.mapa[linha_atual][coluna_atual]
                self.mapa.mapa[linha_atual][coluna_atual] = servidor.EMPTY
                self.mapa.mapa[nova_linha][nova_coluna] = elemento
                return True
            
            else:
                return False
        return False