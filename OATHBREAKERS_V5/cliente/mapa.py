"""
Exemplo de mapa de jogo usando matrizes em Python
Representa um mapa simples com diferentes elementos
"""

class MapaJogo:
    def __init__(self, largura=10, altura=8):
        self.largura = largura
        self.altura = altura
        self.mapa = [['.' for _ in range(largura)] for _ in range(altura)]
        
        # Símbolos do jogo
        self.SIMBOLOS = {
            'vazio': '.',
            'parede': '#',
            'jogador': '@',
            'inimigo': 'E',
            'tesouro': '$',
        }
    
    def adicionar_elemento(self, linha, coluna, tipo):
        """Adiciona um elemento no mapa"""
        if 0 <= linha < self.altura and 0 <= coluna < self.largura:
            self.mapa[linha][coluna] = self.SIMBOLOS[tipo]
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


# ============ EXEMPLO 1: Mapa Estático ============
print("=" * 40)
print("EXEMPLO 1: MAPA ESTÁTICO")
print("=" * 40)

mapa1 = MapaJogo(12, 8)

# Adiciona paredes ao redor
for i in range(mapa1.altura):
    mapa1.adicionar_elemento(i, 0, 'parede')
    mapa1.adicionar_elemento(i, mapa1.largura - 1, 'parede')

for j in range(mapa1.largura):
    mapa1.adicionar_elemento(0, j, 'parede')
    mapa1.adicionar_elemento(mapa1.altura - 1, j, 'parede')

# Adiciona elementos
mapa1.adicionar_elemento(1, 1, 'jogador')
mapa1.adicionar_elemento(3, 3, 'inimigo')
mapa1.adicionar_elemento(2, 5, 'tesouro')

print(mapa1.mapa)

mapa1.exibir_mapa()


# ============ EXEMPLO 2: Mapa com Movimento ============
print("\n" + "=" * 40)
print("EXEMPLO 2: MAPA COM MOVIMENTO")
print("=" * 40)

mapa2 = MapaJogo(10, 6)

# Cria paredes internas
for i in range(1, 5):
    mapa2.adicionar_elemento(i, 3, 'parede')

# Posição inicial do jogador
jogador_linha, jogador_col = 2, 1
mapa2.adicionar_elemento(jogador_linha, jogador_col, 'jogador')
mapa2.adicionar_elemento(4, 8, 'tesouro')

print("\nPosição inicial:")
mapa2.exibir_mapa()

# Simula movimentos
movimentos = [
    (2, 2, "Jogador move para a direita"),
    (3, 2, "Jogador move para baixo"),
    (3, 1, "Jogador move para a esquerda"),
]

for nova_linha, nova_col, descricao in movimentos:
    print(f"\n{descricao}")
    if mapa2.mover_elemento(jogador_linha, jogador_col, nova_linha, nova_col):
        jogador_linha, jogador_col = nova_linha, nova_col
    mapa2.exibir_mapa()


# ============ EXEMPLO 3: Mapa Procedural ============
print("\n" + "=" * 40)
print("EXEMPLO 3: MAPA PROCEDURAL (Aleatório)")
print("=" * 40)

import random

mapa3 = MapaJogo(15, 10)

# Adiciona paredes ao redor
for i in range(mapa3.altura):
    mapa3.adicionar_elemento(i, 0, 'parede')
    mapa3.adicionar_elemento(i, mapa3.largura - 1, 'parede')

for j in range(mapa3.largura):
    mapa3.adicionar_elemento(0, j, 'parede')
    mapa3.adicionar_elemento(mapa3.altura - 1, j, 'parede')


# Adiciona jogador e inimigos
mapa3.adicionar_elemento(1, 1, 'jogador')
for _ in range(3):
    linha = random.randint(1, mapa3.altura - 2)
    coluna = random.randint(1, mapa3.largura - 2)
    if mapa3.mapa[linha][coluna] == '.':
        mapa3.adicionar_elemento(linha, coluna, 'inimigo')

# Adiciona tesouro
linha = random.randint(1, mapa3.altura - 2)
coluna = random.randint(1, mapa3.largura - 2)
if mapa3.mapa[linha][coluna] == '.':
    mapa3.adicionar_elemento(linha, coluna, 'tesouro')

mapa3.exibir_mapa()

# Exibe legenda
print("\nLegenda:")
print("  . = Vazio")
print("  # = Parede")
print("  @ = Jogador")
print("  E = Inimigo")
print("  $ = Tesouro")
print("  T = Árvore")
print("  ~ = Água")
