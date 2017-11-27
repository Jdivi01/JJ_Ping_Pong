#Author: Joe Bender
#Date: 11/26/17

import socket

import PongUtils as utils

'''Wrapper object for tkinter rect screen object'''
class Game_Object():
	
	'''Intitializs the Game_Object'''
	def __init__(self, rect, canvas):
		self.rect = rect
		self.canvas = canvas
		
	'''Get the coordinates of the rect object'''	
	def get_coords(self):
		return self.canvas.coords(self.rect)
	
	'''Updates the coordinates of the rect object'''	
	def set_coords(self, coords):
		self.canvas.coords(self.rect, *coords)
		
	'''Returns string parsed version of coordinates'''
	def parse_coords(self):
		return ':'.join([str(val) for val in self.get_coords()])

'''Handles the client side calls for a pong game'''
class PongClient():
		
	'''Initializes the client, establishes communication with the server'''
	def __init__(self, pong):
		server_addr = ('localhost', 13000)  # connect to the local host
		self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # use TCP protocol		
		self.__client_socket.connect(server_addr)  # Have to establish connection first for TCP
		self.client_id = self.get_client_id()
		self.ball = Game_Object(pong.ball, pong.canvas)
		self.paddle1 = Game_Object(pong.paddle1, pong.canvas)
		self.paddle2 = Game_Object(pong.paddle2, pong.canvas)
		self.net = Game_Object(pong.net, pong.canvas)
		self.win_width = pong.winWIDTH
		
	'''Polls server for client id'''
	def get_client_id(self):
		return int(utils.bytes2string(self.__client_socket.recv(1024)))
		
	'''Create the pong message'''
	def compile_pong_message(self):
		return '%d %s %s %s' % (self.client_id, self.paddle1.parse_coords(), self.ball.parse_coords(), self.net.parse_coords())

	'''Updates the game objects based on the messages sent/received 
	from the server and corresponding PongClient'''
	def update_multiplayer_game_objects(self):
		data_msg = self.compile_pong_message()
		data = self.communicate_with_server(data_msg)
		split_msg = data.split(' ')
		client_id = int(split_msg[0]) #get the received client id
		paddle_coor = self.extract_coords(split_msg[1]) #get the received paddle coords
		paddle2_coor = self.paddle2.get_coords()
		paddle2_coor[1] = paddle_coor[1]
		paddle2_coor[3] = paddle_coor[3]
		self.paddle2.set_coords(paddle2_coor)
		#only update the ball and net values for the newer client
		#this makes the older client be the driver for ball and net values and nothing else
		if client_id > self.client_id:
			ball_coor = self.extract_coords(split_msg[2]) #get the received ball coords
			net_coor = self.extract_coords(split_msg[3]) #get the received net coords
			#invert the ball position to make both user experience similar visuals
			ball_coor[0] = self.win_width - ball_coor[0] 
			ball_coor[2] = self.win_width - ball_coor[2]
			self.ball.set_coords(ball_coor)
			self.net.set_coords(net_coor)
			
	'''Extracts the floating point coordinates from delimited coordinates'''
	def extract_coords(self, string_coord):
		return [float(disp) for disp in string_coord.split(':')]
	
	'''Send data to the server'''
	def communicate_with_server(self, data):
		self.__client_socket.send(utils.string2bytes(data))  # waits to receive data from server
		return  utils.bytes2string(self.__client_socket.recv(1024))  # waits to receive data from server

	'''Destroys the client'''
	def destroy(self):
		self.__client_socket.close()

