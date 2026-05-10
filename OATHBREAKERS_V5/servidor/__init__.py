import socket

EMPTY = '.'
WALL = '#'
PLAYER = '@'
ENEMY = '%'
CHEST =  '$'


COMMAND_SIZE = 10
INT_SIZE = 8
MOVE_UP = "move_up   "
MOVE_DOWN = "move_down "
MOVE_LEFT = "move_left "
MOVE_RIGHT = "move_right"
FIGHT_OP = "fight     "
ATTACK_OP = "attack    "
WAIT_OP = "wait      "
HEAL_OP = "heal      "

BYE_OP = "bye      "
END_OP = "stop     "
PORT = 35000
BROADCAST_PORT = 35001

#Vai buscar diretamente o ip do servidor, para o cliente se conseguir conectar
SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())  
