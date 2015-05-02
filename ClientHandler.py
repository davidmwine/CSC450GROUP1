import threading
import re
import Server


class ClientHandler(object):
    def __init__(self, cmd, add):
        ##receive cmd - this will be a full string
        print("handler has ", cmd)
        self.tCnt = 1## initially used as a thread count
        self.address = add ## assign the address
        self.cmd = cmd ## assign the cmd
    
    def run(self):
        print("handler running with ", self.cmd)## show what youre working with
        cmdList = self.cmd.split(" ")## split into list
        print(cmdList)## show your list
        myCmd = cmdList[0]## first value in list should be cmd
        args = cmdList[1:-1]## everything else is an argument
        try:
            ## pass string as function
            result = getattr(self, myCmd)(args)
            ## client will use this
            return result
        except:
            ##if the cmd is not defined it will return what it received
            return myCmd
    ########
    ##define functions here - these are examples for now
    ## should be able to cal functions from other programs
    ########
    def join(self):
        return "Joining"

    def chat(self):
        msg = "handling chat"
        print(msg)
        return msg
        
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

