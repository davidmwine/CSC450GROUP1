import threading
import re
import Server_1

#allClients = getGlobalClients()
#print("From handler Global Clients: ", allClients)
gameClients = [] # this is for individual games
#globalClients= [] # this is for the main loby area
tCnt = 0
#globals = [tCnt, globalClients]

##def getGameClients():
##    '''
##    Returns a list of all clients trying to make a game
##    '''
##    return gameClients
##
##def getGlobalClients():
##    print("attempting to get global clients list")
##    return globalClients

##def setTCnt():
##    tCnt += 1
##    
##def getTCnt():
##    return tCnt

def joinMainLobby(client):
    print("attempting to enter global lobby")
    globalClients.append(client)

## append to flie client info
## consider making a string object to append to this file
##def addGlobalClient(client):
##    print("attempting to get global clients list")
##    myFile = open("globalClientsList.txt", "a+")
##    clients = []
##    while myFile.readline():
##        c = myFile.readline()
##        clients.append(c)
##    if client not in clients:
##        print("adding client ", client)
##        myFile.write(str(client)+"\n")## convert to a string to write to the file
##    #myFile.write("\n")
##    myFile.close()

## this will be a string you need to convert back to an address
## you need to fix how this is getting the numbers - find a better method
def reclaimAddress(client):
    if client != "":
        client = client.split(" ")
        ipAdd = client[0]
        ipAdd = ipAdd[2:-2]
        print("ipadd ", ipAdd)
        port = client[1]
        port = port[0:-2]
        print("port ", port)
        client = (ipAdd, int(port))
        return client
    

##def addGameClient(client):
##    print("attempting to get game clients list")
##    print >> gameClientsList.txt, client

class ServerHandler(object):
    #tCnt = 1
    #clientsCount = 0
    def __init__(self, cmd, add):
        print("handler has ", cmd)
        self.tCnt = 1
        self.address = add
        self.cmd = cmd
    
    def run(self):
        print("handler running with ", self.cmd)
        cmdList = self.cmd.split(" ")
        print(cmdList)
        myCmd = cmdList[0]
        args = cmdList[1:-1]
        try:
            result = getattr(self, myCmd)(args)## pass string to function call form
        except:
            return myCmd
        
##    def thread(self):
##        print("handling thread")
##        name = "thread " + str(self.tCnt)
##        #clientsCount += 1
##        thread = threading.Thread(name = "Thread-{}".format(len(globalClients)+1))
##        thread.daemon = True
##        thread.start()
##        print(thread.name, " now open.")
##        self.tCnt += 1

    def join(self):
        return "Joining"

    def chat(self):
        print("handling chat")
    def getGlobals(self):
        print("global clients ", Server_1.globalClients)

    def clearGlobals(self):
        Server_1.globalClients = []

    def leaveGlobals(self):
        myFile = open('globalClientsList.txt', 'a+')
        
        c = myFile.readlines()
        for client in c:
            if client != self.address:
                myFile.write(client + "\n")
        myFile.close()
        

    def diceRoll(self):
        print("dice cmd")
        
        
    def close(self):
        print("closing thread", self.address)
        if self.address in globalClients:
            globalClients.remove(self.address)
        thread.close()

