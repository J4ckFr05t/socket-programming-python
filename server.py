import socket
import sys
from _thread import *
import threading
import time
from termcolor import colored   #for highlighting

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    IP_address = "127.0.0.1"
    Port = 8081
except:
    print(colored("[STATUS]",'green'),end="")
    print(colored(" Unable to start server. Try changing the port",'white'))
    sys.exit()

all_threads = [] 
server.bind((IP_address, Port))
print(colored("[INFO] ",'green'),end="")
print(colored("Server running on port "+str(Port),'white'))
server.listen(100) 
list_of_clients = [] 
  
def clientthread(conn, addr):
    while True: 
            try: 
                message = conn.recv(2048)
                if message.decode()!="exit":
                    message_to_send = message.decode()
                    broadcast(message_to_send.encode(), conn) 
  
                elif message.decode() == "exit":
                    print(colored("[INFO] ",'green'),end="")
                    print(colored(str(addr[0])+":"+str(addr[1]),'cyan'),end="")
                    print(colored(" left the server",'white'))
                    esms = "exit"
                    conn.send(esms.encode())
                    remove(conn)
                    break
  
            except: 
                continue

def broadcast(message, connection):
    print(colored("[Send]",'cyan'),end="")
    print(colored(" Broadcastig message ",'white'),end="")
    print(colored("' "+message.decode()+" '",'white'))
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close()
                remove(clients)
  
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection)

def shutdown():
    while True:
        cmd = input()
        if cmd == "quit":
            print(colored("[STATUS] ",'green'),end="")
            print(colored("Shuting down server",'yellow'))
            for client in list_of_clients:
                client.send(cmd.encode())
            print(colored("[INFO] ",'green'),end="")
            print(colored("waiting for all clients to exit before shutdown",'white'))
            server.close()
            break
        else:
            print(colored("[STATUS] ",'green'),end="")
            print(colored("Server Running",'white'))

sd = threading.Thread(target=shutdown)
sd.start()
  
while True:
    try:
        conn, addr = server.accept() 
        list_of_clients.append(conn) 
        print(colored("[INFO] ",'green'),end="")
        print(colored(str(addr[0])+":"+str(addr[1]),'cyan'),end="")
        print (colored(" appeared in the server",'white'))
        t=threading.Thread(target=clientthread,args=(conn,addr))
        all_threads.append(t)
        t.start()
    except:
        break

for th in all_threads:
    th.join()
sd.join()
print(colored("\n[STATUS] ",'green'),end="")
print(colored("Server has shutdown",'white'))