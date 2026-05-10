import random
import servidor
"""
Exemplo de mapa de jogo usando matrizes em Python
Representa um mapa simples com diferentes elementos
"""

class MapaJogo:
    def __init__(self, largura=10, altura=8):
        self.largura = largura
        self.altura = altura
        self.mapa = [['.' for _ in range(largura)] for _ in range(altura)]
        

        # Adiciona paredes ao redor
        for i in range(self.altura):
            self.adicionar_elemento(i, 0, servidor.WALL)
            self.adicionar_elemento(i, self.largura - 1, servidor.WALL)

        for j in range(self.largura):
            self.adicionar_elemento(0, j, servidor.WALL)
            self.adicionar_elemento(self.altura - 1, j, servidor.WALL)
        
        # Adiciona jogador e inimigos
        for _ in range(3):
            linha = random.randint(1, self.altura - 2)
            coluna = random.randint(1, self.largura - 2)
            if self.mapa[linha][coluna] == '.':
                self.adicionar_elemento(linha, coluna, servidor.ENEMY)

        # Adiciona tesouro
        linha = random.randint(1, self.altura - 2)
        coluna = random.randint(1, self.largura - 2)
        if self.mapa[linha][coluna] == '.':
            self.adicionar_elemento(linha, coluna, servidor.CHEST)
        

        self.exibir_mapa()

            
    def adicionar_elemento(self, linha, coluna, tipo):
        """Adiciona um elemento no mapa"""
        if 0 <= linha < self.altura and 0 <= coluna < self.largura:
            self.mapa[linha][coluna] = tipo
            return True
        return False
    
    def exibir_mapa(self):
        """Exibe o mapa no terminal"""
        # Exibe numeração das colunas
        print("  ", end="")
        for c in range(self.largura):
            print(f"{c} ", end="")
        print()
        
        # Exibe cada linha com sua numeração
        for i, linha in enumerate(self.mapa):
            print(f"{i} ", end="")
            for celula in linha:
                print(f"{celula} ", end="")
            print()
    
    def mover_elemento(self, linha_atual, coluna_atual, nova_linha, nova_coluna):
        """Move um elemento de uma posição para outra"""
        if 0 <= nova_linha < self.altura and 0 <= nova_coluna < self.largura:
            # Verifica se destino não é parede
            if self.mapa[nova_linha][nova_coluna] != '#':
                elemento = self.mapa[linha_atual][coluna_atual]
                self.mapa[linha_atual][coluna_atual] = '.'
                self.mapa[nova_linha][nova_coluna] = elemento
                return True
        return False
    
    def obter_elemento(self, linha, coluna):
        """Retorna o elemento em uma posição"""
        if 0 <= linha < self.altura and 0 <= coluna < self.largura:
            return self.mapa[linha][coluna]
        return None

