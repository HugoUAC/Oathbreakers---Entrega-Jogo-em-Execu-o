import random

class Luta:
    def __init__(self, connection, address, dados):
        self.connection = connection
        self.address = address
        self.dados = dados
        self.players = self.dados.get_players_info()
        self.enemies = self.dados.inimigos
        self.classes = self.dados.classes
        random.shuffle(self.enemies)
        self.enemy = self.enemies[0].copy()

    def luta(self, player1, player2=None):
        if player2 is None:
            if self.luta_um_jogador(player1):
               return True
            return False
        else:
            if self.luta_dois_jogadores(player1, player2):
                return True
            return False

    def luta_um_jogador(self,player):
        for key, value in player.items():
            for classe in self.classes:
                if key == "classe":
                    if classe["nome"] == value:
                        player_attack = classe["ataque"]

            # Luta contra inimigo
        while player["vida"] > 0 and self.enemy["vida"] > 0:
            # Player ataca inimigo
            damage_to_enemy = random.randint(7, player_attack)  # Exemplo de dano
            self.enemy["vida"] -= damage_to_enemy
            print(f"{player['nome']} atacou {self.enemy['nome']} causando {damage_to_enemy} de dano!")

            if self.enemy["vida"] <= 0:
                print(f"{player['nome']} venceu a luta contra {self.enemy['nome']}!")
                self.dados.atualizar_player(self.address, player)
                self.dados.players_fight.clear()
                return True

            # Inimigo ataca player
            damage_to_player = random.randint(5, self.enemy["ataque"])  # Exemplo de dano
            player["vida"] -= damage_to_player
            print(f"{self.enemy['nome']} atacou {player['nome']} causando {damage_to_player} de dano!")

            if player["vida"] <= 0:
                print(f"{self.enemy['nome']} venceu a luta contra {player['nome']}!")
                self.dados.atualizar_player(self.address, player)
                self.dados.players_fight.clear() 
                return False
            
    def luta_dois_jogadores(self, player1, player2):
        for key, value in player1.items():
            for classe in self.classes:
                if key == "classe":
                    if classe["nome"] == value:
                        player1_attack = classe["ataque"]
        for key, value in player2.items():
            for classe in self.classes:
                if key == "classe":
                    if classe["nome"] == value:
                        player2_attack = classe["ataque"]

        while player1["vida"] > 0 or player2["vida"] > 0 and self.enemy["vida"] > 0:
            # Player1 ataca inimigo
            if player2["vida"] <= 0:
                pass
            else:
                damage_to_enemy = random.randint(7, player1_attack)  # Exemplo de dano
                self.enemy["vida"] -= damage_to_enemy
                print(f"{player1['nome']} atacou {self.enemy['nome']} causando {damage_to_enemy} de dano!")

            if self.enemy["vida"] <= 0:
                print(f"{player1['nome']} venceu a luta contra {self.enemy['nome']}!")
                self.dados.players_fight.clear()
                return True

            # Inimigo ataca um player
            damage_to_player = random.randint(5, self.enemy["ataque"])  # Exemplo de dano
            player_atacked = random.choice([player1, player2])
            if player_atacked["vida"] <= 0:
                player_atacked = player1 if player_atacked == player2 else player2
            player_atacked["vida"] -= damage_to_player
            print(f"{self.enemy['nome']} atacou {player_atacked['nome']} causando {damage_to_player} de dano!")

            if player1["vida"] <= 0 and player2["vida"] <= 0:
                print(f"{self.enemy['nome']} venceu a luta contra {player1['nome']} e contra {player2['nome']}!")
                self.dados.players_fight.clear()
                return False

            # Player2 ataca inimigo
            if player2["vida"] <= 0:
                pass
            else:
                damage_to_enemy = random.randint(7, player2_attack)  # Exemplo de dano
                self.enemy["vida"] -= damage_to_enemy
                print(f"{player2['nome']} atacou {self.enemy['nome']} causando {damage_to_enemy} de dano!")

            if self.enemy["vida"] <= 0:
                print(f"{player2['nome']} venceu a luta contra {self.enemy['nome']}!")
                self.dados.players_fight.clear()
                return True
        