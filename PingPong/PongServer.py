#Author: Joe Bender
#Date: 11/26/17

import socket

import PongUtils as utils

'''Sets up the server for multi-player pong'''
class PongServer():
	
	'''Giving credit where due: 
	https://stackoverflow.com/questions/33434007/python-socket-send-receive-messages-at-the-same-time
	Used to figure out simultaneous send/receive on same socket using threads'''
	
	client_index = 0 #used to id sockets
	
	'''Starts the server'''
	def __init__(self):
		server_addr = ('localhost', 13000) #host server (locally)
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #use TCP protocol
		self.server_socket.bind(server_addr)
		self.server_socket.listen(5) #means we are running, and can receive messages	
		self.playerA_socket = None
		self.playerB_socket = None
		self.listen_for_sockets()
	
	'''Constant polling for sockets, connects pairs to form connection for Pong game'''
	def listen_for_sockets(self):
		while True:
			client_socket, attr = self.server_socket.accept() #accept new client_sockets
			if not self.playerA_socket:
				self.playerA_socket = client_socket
				self.send_client_id(self.playerA_socket) #send id to player A socket
				utils.run_thread(self.wait_for_player_B_connection, (self.playerA_socket, self.client_index)) #create listener threads
			elif not self.playerB_socket:
				self.playerB_socket = client_socket
				self.send_client_id(self.playerB_socket) #send id to player B socket
			if self.playerA_socket and self.playerB_socket:
				utils.run_thread(self.recieve, (self.playerA_socket, self.playerB_socket)) #create listener threads
				utils.run_thread(self.recieve, (self.playerB_socket, self.playerA_socket)) #create listener threads
				self.playerA_socket = None
				self.playerB_socket = None
	
	'''Sends 'N' to player A socket, signifying that a player B has not joined the server yet'''
	def wait_for_player_B_connection(self, playerA_socket, playerA_id):
		while self.client_index <= playerA_id:			
				data = playerA_socket.recv(1024) # wait for PongClient to send data
				if data:
					playerA_socket.send(utils.string2bytes('N'))
				if utils.bytes2string(data) is 'X':
					self.playerA_socket = None
					break #terminate thread when the socket sends an 'X' indicating that the socket is beiong closed	
				
	'''Sends the client id to the socket'''
	def send_client_id(self, client_socket):
		client_socket.send(utils.string2bytes(str(self.client_index)))
		self.client_index += 1
	
	'''Setup protocol for receiving data from socket A to socket B'''
	def recieve(self, playerA_socket, playerB_socket):	
		while True:		
			data = playerA_socket.recv(1024) # wait for PongClient to send data				
			
			if data:
				if utils.bytes2string(data) is 'W':
					utils.run_thread(self.send, (playerB_socket, utils.string2bytes('L')))
				elif utils.bytes2string(data) is 'L':
					utils.run_thread(self.send, (playerB_socket, utils.string2bytes('W')))
				else:
					utils.run_thread(self.send, (playerB_socket, data))
					if utils.bytes2string(data) is 'X':
						break #terminate thread when the socket sends an 'X' indicating that the socket is beiong closed
				
	'''Sends bytes to the output socket'''
	def send(self, playerB_socket, data):
		playerB_socket.send(data)
			
	'''Closes the server's socket'''
	def destroy(self):
		self.server_socket.close()
	
if __name__ == '__main__':
	server = PongServer()
