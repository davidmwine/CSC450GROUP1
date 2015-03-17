from socket import *
import socketserver
import threading
from ServerHandler_v1_2 import *

# Use these for binding our server
#when ready for WAN testing replace with:
#socket.gethostbyname(socket.gethostname()) ##ip x.x.x.x
HOST = ""
PORT = 10205
globalClients = []
gameClients = []
#globals = [globalClients, gameClients]


def addGlobalClient(client):
    if client not in globalClients:
        globalClients.append(client)

def getGlobalClients():
    print(globalClients)

def joinGameClients(client):
    if client not in gameClients:
        globalClients.remove(client)
        gameClients.append(client)


class MyThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("Starting ", self.name, ". With ID ", self.threadID, ". And counter of ", self.counter)

##class PlayersList(object):
##        def __init__(self, pList):
##            self.plist = clientsList
##        def addToPList(self):
##            clientsList.append(self)
##
##def enterMainLobby():

def moveToGameLobby(adress):
    if address in globalClients:
        gameClients.append(address)
        globalClients.remove(address)

## check to make sure the clients still have connectivity
## otherwise delete them from the list
## consider making another function which runs this as a thread every 5 seconds
def pingClients():
    print("attempting ping clients list")
    while True:
        message, address = server.recvfrom(1024)
        file = open('globalClientsList.txt', 'r+')
        with file as addresses:
            for client in addresses:
                try:
                    client = reclaimAddress(client)
                    message = "PINGING CLIENT THREAD"
                    server.sendto(message.encode(), client)
                    ##print("sending to:", client)
                except:
                    print("unable to read from client.")           
            file.close()
    

## Create the server
def runServer():
    server = socket(AF_INET, SOCK_DGRAM)
    server.bind((HOST, PORT))

    while(True):
        print("Client List: ", globalClients)
        try:
            message, address = server.recvfrom(1024)
        except:
            globalClients.remove(address)
            continue
        print("Receiving: '", message.decode(),"'. From: ", address)
        handler = ServerHandler(message.decode(), address)
        addGlobalClient(address)
        this = handler.run()
        print("this", this)
            
        if message.decode() == "shutdown":
            print("You received the shutdown command.")
            server.shutdown()
            
    ##File Method    print("attempting to get clients list")
    ##    file = open('globalClientsList.txt', 'r+')
    ##    with file as this:
    ##        for client in this:
    ##            #print("client before:", client)
    ##            client = reclaimAddress(client)
    ##            #print("client after:", client)
    ##            #client = tuple(client)
    ##            try:
    ##                server.sendto(message.upper(), client)
    ##                print("sending to:", client)
    ##            except error:
    ##                print("unable to read.", error)
    ##        file.close()
        for player in globalClients:
                server.sendto(message.upper(), player)
        print("\n","\n")

if __name__ == "__main__":
    runServer()
