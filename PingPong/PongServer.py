#Author: Joe Bender
#Date: 11/26/17

import socket

import PongUtils as utils

'''Sets up the server for multi-player pong'''
class PongServer():
	
	client_index = 0 #used to id sockets
	
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
				self.send_client_id(playerA_socket) #send id to player A socket
				utils.run_thread(self.wait_for_player_B_connection, (playerA_socket, self.client_index)) #create listener threads
			elif not playerB_socket:
				playerB_socket = client_socket
				self.send_client_id(playerB_socket) #send id to player B socket
			
			if playerA_socket and playerB_socket:
				utils.run_thread(self.recieve, (playerA_socket, playerB_socket)) #create listener threads
				utils.run_thread(self.recieve, (playerB_socket, playerA_socket)) #create listener threads
				playerA_socket = None
				playerB_socket = None
				
	'''Sends 'N' to player A socket, signifying that a player B has not joined the server yet'''
	def wait_for_player_B_connection(self, playerA_socket, playerA_id):
		while self.client_index <= playerA_id:			
				data = playerA_socket.recv(1024) # wait for PongClient to send data
				if data:
					playerA_socket.send(utils.string2bytes('N'))
	
	'''Sends the client id to the socket'''
	def send_client_id(self, client_socket):
		client_socket.send(utils.string2bytes(str(self.client_index)))
		self.client_index += 1
	
	'''Setup protocol for receiving data from socket A to socket B'''
	def recieve(self, playerA_socket, playerB_socket):		
		try:			
			while True:			
				data = playerA_socket.recv(1024) # wait for PongClient to send data
				if data:
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
