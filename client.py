from _thread import *
import threading
import socket
from termcolor import colored   #for highlighting

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1',8081))
print(colored("\n-----Welcome to Jibins Chat Room------\n",'cyan'))
hostname = input("Enter a display name: ")
print("\n")
hostname = hostname+"\t: "
def send():
	while True:
		message=input("You\t: ")
		if message == 'exit':
			sock.send(message.encode())
			break
		else:
			msg = hostname+message
			sock.send(msg.encode())

def receive():
	while True:
		message = sock.recv(2048)
		if message.decode() == "quit":
			print(colored("\n[INFO]",'green'),end="")
			print(colored("Server shutting down. Type exit\n$:",'white'),end="")
			break
		elif message.decode() == "exit":
			print("\nBye ",hostname[:-3])
			break
		else:
			print("\n"+colored(message.decode(),'white'),end="")
			print('\nYou\t: ',end="")
	
	
t1 = threading.Thread(target =  send)
t1.start()
t2 = threading.Thread(target = receive)
t2.start()

t1.join()
t2.join()
sock.close()
