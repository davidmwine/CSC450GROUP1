import threading
import re
import Server


class ServerHandler(object):
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
            return result
        except:
            return myCmd

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

