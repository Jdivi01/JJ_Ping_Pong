#Author: Joe Bender
#Date: 11/26/17

''''Utilities for common logic'''
from threading import Thread

'''Creates and runs new thread which excecutes the input function'''		
def run_thread(func, func_args):
	Thread(target=func, args=func_args).start()

'''Convert String to Byte array'''
def string2bytes(text):
	return bytes(text, "utf8")
	
'''Convert Byte array to String'''
def bytes2string(input_bytes):
	return str(input_bytes, "utf8")
