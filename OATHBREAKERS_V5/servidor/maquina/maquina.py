from servidor.dados.dados import Dados
from servidor.operacoes.mapa import MapaJogo
from servidor.maquina.processa_cliente import ProcessaCliente
from servidor.maquina.broadcast_emissor import ThreadBroadcast
import servidor
import socket

class Maquina:
	def __init__(self):
		self.dados = Dados()
		self.s = socket.socket()
		self.s.bind(('', servidor.PORT))
		self.broadcast = None
		self.mapa = MapaJogo(12,10)


	def execute(self):
		print("Starting server on " + servidor.SERVER_ADDRESS + ":" + str(servidor.PORT))

		self.broadcast = ThreadBroadcast(mapa=self.mapa, dados=self.dados, intervalo=5)
		self.broadcast.start()

		self.s.listen(5)
		print("Waiting for clients on port " + str(servidor.PORT))
		try:
			while True:
				print("On accept...")
				connection, address = self.s.accept()
				print("Client " + str(address) + " connected")
				ProcessaCliente(connection, address, self.dados, self.mapa).start()
		except KeyboardInterrupt:
			print("Stopping...")
		finally:
			self.s.close()
			self.broadcast.running = False
			print("Server stopped")
