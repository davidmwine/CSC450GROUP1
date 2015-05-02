import sys
from socket import *
from select import *
#import socketserver
import threading
from queue import *
from ServerHandler import *

##globals for server and client handling
HOST = "127.0.0.1"
PORT = 10205
BUFFER = 4096
globalClients = []
games = []
cmdList = Queue(maxsize = 0)

## Send any incoming message to all clients connected to the server
def broadcast(server, message):
    print("Broadcasting:",message,". To", len(globalClients)-1, "users.")
    for socket in globalClients:
        if len(message) < 1:
            break
        else:
            if socket != server: ## omit the server from clients list
                try:
                    ##message should already be a string
                    message = str(message) ## not necessary but may be useful
                    socket.send(message.encode())
                except:
                    socket.close() ## Unable to communicate with the client
                    if socket in globalClients:
                        globalClients.remove(socket)
    print("leaving broadcast\n\n")

def isInGame(sockfd):
    for i in games:
        for j in i:
            if j[0].getpeername() == sockfd.getpeername():
                return True
    return False
 
def gameServer():
    ## Create the server
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(100)## Can handle up to 100 clients simultaneously
    globalClients.append(server)# the server will receive info too
    print("Game server is now running.\
           \nWaiting for connections......")

    while(True):
        ##select for read.... we will manually write by command
        read, write, err = select(globalClients, [], [])

        ##allow all users to write to the server
        for sock in read:
            ##if the incomming socket has server address its new
            if sock == server:
                ##connect the new client to the server
                sockfd, addr = server.accept()
                globalClients.append(sockfd)
                message = "Client %s %s has connected" % addr
                print(message, "\n")
                ##only use this broadcast for debugging only
                broadcast(server, message)

            ##else a user is trying to send data to the server
            else:
                ##receive the data
                try:
                    data = sock.recv(BUFFER)
                    data = data.decode()
                    ##process the data
                    if data and len(data) > 1:
                        print("getting data ", data)
                        ##send the data to the serverhandler
                        ##the server handler will do the work
                        ##action return what we need
                        handler = ServerHandler(data, sockfd)
                        action = handler.run()
                        print("after handler.run: ", action)
                        ##send the action to all user
                        if isInGame(sockfd):
                            for i in games:
                                for j in i:
                                    if j[0].getpeername() == sockfd.getpeername() and i[4] == True:
                                        broadcast(i, action)
                        else:
                            broadcast(server, action)
                        
                    else:
                        ##detect if a user is still connected
                        if sock in globalClients:
                            globalClients.remove(sock)
                            broadcast(server, "Client (%s, %s) is offline\n" % sock)
                except:
                    ##detect if a user had chosen to leave
                    if sock in globalClients:
                        globalClients.remove(sock)
                    broadcast(server, "Client (%s, %s) went offline" % addr)
                    continue
    ##no more use for connections, break all processes, server side
    ##this will make you client go into an infinite receive if still connected
    ##ie the sever has crashed
    server.close()


if __name__ == "__main__":
    sys.exit(gameServer())
