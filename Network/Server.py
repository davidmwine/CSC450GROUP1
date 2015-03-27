import sys
from socket import *
from select import *
#import socketserver
import threading
#from ServerHandler import *

# Use these for binding our server
# when ready for WAN testing replace with:
# socket.gethostbyname(socket.gethostname()) ##ip x.x.x.x
HOST = "127.0.0.1"
PORT = 10205
BUFFER = 4096
globalClients = []
gameClients = []

## Send any incoming message to all clients connected to the server
def broadcast(server, message):
    ## special case: if only 1 user it will say broadcasting to 2 users
    ## when first connecting, aside from very first connection
    print("Broadcasting:",message,". To", len(globalClients)-1, "users.")
    for socket in globalClients:
        if len(message) < 1:
            break
        else:
            if socket != server: ## omit the server from clients list
                try:
                    message = str(message) ## not necessary but may be useful
                    socket.send(message.encode())
                except:
                    socket.close() ## Unable to communicate with the client
                    if socket in globalClients:
                        globalClients.remove(socket)
    print("leaving broadcast")
  

## Create the server
def gameServer():
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(100)## Can handle up to 100 clients simultaneously
    globalClients.append(server)# the server will receive info too
    print("Game server is now running.\
           \nWaiting for connections......")

    while(True):
        #read, write, err = select(globalClients, [], [])
        ##print("Client List: ", globalClients)

        for sock in globalClients:
            if sock == server:
                sockfd, addr = server.accept()
                globalClients.append(sockfd)
                message = "Client %s %s has connected" % addr
                print(message)
                broadcast(server, message)

            else:#incomming data to server
                try:
                    data = sock.recv(BUFFER)
                    data = data.decode()
                    if data and len(data) > 1:
                        print("getting data ", data)
                        broadcast(server, data)
                    else:
                        if sock in globalClients:
                            globalClients.remove(sock)
                            broadcast(server, "Client (%s, %s) is offline\n" % sock)
                except:
                    if sock in globalClients:
                        globalClients.remove(sock)
                    broadcast(server, "Client (%s, %s) went offline" % addr)
                    continue
    server.close()


if __name__ == "__main__":
    sys.exit(gameServer())
