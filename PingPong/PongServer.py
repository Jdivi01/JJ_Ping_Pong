'''Sets up a local Pong Server'''

'''Sets up the server for multi-player pong'''

import socket

import PongUtils as utils


class PongServer():
	
	'''Starts the server'''
	def __init__(self):
		server_addr = ('localhost', 13000) #host server (locally)
		self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #use TCP protocol
		self.__server_socket.bind(server_addr)
		self.__server_socket.listen(5) #means we are running, and can receive messages	
		playerA_socket = None
		playerB_socket = None
		while True:		
			client_socket, attr = self.__server_socket.accept() #accept new client_sockets
			if not playerA_socket:
				playerA_socket = client_socket
			elif not playerB_socket:
				playerB_socket = client_socket
			
			if playerA_socket and playerB_socket:
				utils.run_thread(self.recieve, (playerA_socket, playerB_socket))
				utils.run_thread(self.recieve, (playerB_socket, playerA_socket))
				playerA_socket = None
				playerB_socket = None
	
	def recieve(self, playerA_socket, playerB_socket):		
		try:			
			while True:			
				data = playerA_socket.recv(1024) # wait for PongClient to send data
				if data:
					if utils.bytes2string(data) is 'w':
						utils.run_thread(self.send, (playerA_socket, "YOU WON! NIIIICE"))
						utils.run_thread(self.send, (playerB_socket, "YOU LOST! HAHAH"))
					else:	
						utils.run_thread(self.send, (playerB_socket, data))
		except ConnectionResetError:
			return
			
	'''Sends bytes to the output socket'''
	def send(self, playerB_socket, data):
		playerB_socket.send(data)
			
	'''Closes the server's socket'''
	def destroy(self):
		self.__sever_socket.close()
	
if __name__ == '__main__':
	server = PongServer()
