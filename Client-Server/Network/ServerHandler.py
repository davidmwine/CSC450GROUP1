import threading

gameClients = [] # this is for individual games
globalClients= [] # this is for the main loby area
tCnt = 0
globals = [tCnt, globalClients]

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
def addGlobalClient(client):
    print("attempting to get global clients list")
    myFile = open("globalClientsList.txt", "r+")
    myFile.write(str(client)+"\n")## convert to a string to write to the file
    #myFile.write("\n")
    print(myFile.read())
    myFile.close()

## this will be a string you need to convert back to an address
def reclaimAddress(client):
    split = client.split(" ")
    ipAdd = client[2:-10]
    #print(ipAdd)
    port = client[-7:-2] ## remember to convert to int
    #print(port)
    client = (ipAdd, int(port))
    return client
    

##def addGameClient(client):
##    print("attempting to get game clients list")
##    print >> gameClientsList.txt, client

class ServerHandler:
    #tCnt = 1
    #clientsCount = 0
    def __init__(self, cmd, add):
        print("handler has ", cmd)
        self.tCnt = 1
        self.address = add
        self.cmd = cmd

##    ## append to flie
##    def addGlobalClient(client):
##        print("attempting to get global clients list")
##        print >> globalClientsList, client
##
##    def addGameClient(client):
##        print("attempting to get game clients list")
##        print >> gameClientsList, client

##    def getGlobalClients():
##        print("attempting to get global clients list")
##        return globalClients
    
    def run(self):
        print("handler running with ", self.cmd)
        cmdList = self.cmd.split(" ")
        print(cmdList)
        
        if self.cmd == "thread":
            print("handling thread")
            name = "thread " + str(self.tCnt)
            #clientsCount += 1
            thread = threading.Thread(name = "Thread-{}".format(len(globalClients)+1))
            thread.daemon = True
            thread.start()
            #addGlobalClient(thread)
            print(thread.name, " now open.")
            self.tCnt += 1
            return thread
            
        if self.cmd == "getGlobals":
            myFile = open('globalClientsList.txt', 'r')
            allClients = []
            with myFile as this:
                for client in this:
                    allClients.append(client)
            myFile.close()
            return allClients

        if self.cmd == "clearGlobals":
            open('globalClientsList.txt', 'w').close()
            myFile = open('globalClientsList.txt', 'r+')
            myFile.seek(0)
            myFile.truncate()
            myFile.close()
            

        if self.cmd == "diceRoll":
            print("dice cmd")
            
            
        if self.cmd == "close":
            print("closing thread", self.address)
            if self.address in globalClients:
                globalClients.remove(self.address)
            thread.close()

