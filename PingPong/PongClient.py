
'''Creates and handles Client connection with server'''

import socket

import PongUtils as utils


class PongClient():
	
	def __init__(self, paddle1, paddle2):
		server_addr = ('localhost', 13000) #connect to the local host
		self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #use TCP protocol		
		self.__client_socket.connect(server_addr) #Have to establish connection first for TCP
		self.paddle1 = paddle1
		self.paddle2 = paddle2
		
	def update_mulitplayer_game_objects(self):
		data_msg = str(self.paddle1.paddle_height_var.get())
		data = self.communicate_with_server(data_msg)
		if 'W' in data:
			return data
		elif 'L' in data:
			return data			
		self.paddle2.paddle_height_var.set(int(data))
		return None
	
	'''Send data to the server'''
	def communicate_with_server(self, data):
		self.__client_socket.send(utils.string2bytes(data)) #waits to receive data from server
		return  utils.bytes2string(self.__client_socket.recv(1024)) #waits to receive data from server

	def destroy(self):
		self.__client_socket.close()





