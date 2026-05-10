import socket
import json
import time
import cliente
from cliente.broadcast_receiver import BroadcastReceiver

class Interface:
	def __init__(self):
		self.connection = socket.socket()
		self.ip = input("Insira o endereço IP do servidor: ")
		self.connection.connect((self.ip, cliente.PORT))

		self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket dedicada ao broadcast
		self.broadcast_socket.bind(('', 0))
		self.broadcast_port = self.broadcast_socket.getsockname()[1] 

		self.send_int(self.connection, self.broadcast_port, cliente.INT_SIZE)
		print(f"Cliente ligado por TCP/IP mas à escuta de mensagens por UDP na porta {self.broadcast_port}")
		print(self.broadcast_socket)
		broadcast = BroadcastReceiver(self.broadcast_socket)
		broadcast.start()
#--------- Funções de envio e receção de dados ---------

	def receive_str(self,connect, n_bytes: int) -> str:
		data = connect.recv(n_bytes)
		return data.decode()

	def send_str(self,connect, value: str) -> None:
		connect.send(value.encode())

	def send_int(self,connect:socket.socket, value: int, n_bytes: int) -> None:
		connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

	def receive_int(self,connect: socket.socket, n_bytes: int) -> int:
		data = connect.recv(n_bytes)
		return int.from_bytes(data, byteorder='big', signed=True)

	def send_object(self,connection, obj):
		"""1º: envia tamanho, 2º: envia dados."""
		data = json.dumps(obj).encode('utf-8')
		size = len(data)
		self.send_int(connection, size, cliente.INT_SIZE)
		connection.send(data)

	def receive_object(self,connection):
		"""1º: lê tamanho, 2º: lê dados."""
		size = self.receive_int(connection, cliente.INT_SIZE)
		data = connection.recv(size)
		return json.loads(data.decode('utf-8'))

#--------------------------------------------------------

	def execute(self):

		self.connection.settimeout(2)

		player_name = input("\nInsira o nome do jogador (MAX 10 chars): ")
		player_name_padded = player_name[:10].ljust(10)
		self.send_str(self.connection, player_name_padded)

		print("\nPreciso que escolha uma das classes apresentadas:")
		classes = self.receive_object(self.connection)

		counter = 1
		while True:
			for classe in classes:
				print(f"{counter} - {classe['nome']} - {classe['descricao']}")
				counter += 1

			option = input()

			if option.isdigit() and 1 <= int(option) <= len(classes):
				selected_class = classes[int(option) - 1]
				self.send_object(self.connection, selected_class)
				print(f"Você escolheu a classe: {selected_class['nome']}")
				break
			else:
				print("Opção inválida. Por favor, escolha um número válido.\n")
				counter = 1

		while True:
				try:
					if self.receive_str(self.connection,cliente.INT_SIZE) == cliente.ENEMY:
						if self.receive_int(self.connection,cliente.INT_SIZE) == 0:
							print("\nINIMIGO ENCONTRADO!")
							print("Aguardar companheiro (W) ou Atacar sozinho (A)?")
							
							choice = input().lower()
							if choice == "w":
								print("À espera do companheiro...")
								self.send_str(self.connection, cliente.WAIT_OP)
								time.sleep(30)
							elif choice == "a":
								print("A atacar o inimigo...")
								self.send_str(self.connection, cliente.ATTACK_OP)
								time.sleep(30)
						else:
							time.sleep(30)
				except:
					pass

				print("Indique a posição por onde quer ir (W,A,S ou D) e pressione enter ('.' para fim)\n")
				res:str = input().lower().strip()
				if res == "":
					continue
				if res == "w":
					self.send_str(self.connection, cliente.MOVE_UP)
				if res == "s":
					self.send_str(self.connection, cliente.MOVE_DOWN)
				if res == "a":
					self.send_str(self.connection, cliente.MOVE_LEFT)
				if res == "d":
					self.send_str(self.connection, cliente.MOVE_RIGHT)
				
				if res == "h":
					self.send_str(self.connection, cliente.HEAL_OP)
					
				if res == ".":
					self.send_str(self.connection, cliente.BYE_OP)
					print("Encerrando conexão.")
					self.connection.close()
					self.broadcast_socket.close()
					break

				if res == "sys_out":
					self.send_str(self.connection, cliente.END_OP)
					print("Fechando servidor e encerrando conexão.")
					self.connection.close()
					self.broadcast_socket.close()
					break
