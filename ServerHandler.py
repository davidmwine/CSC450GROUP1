import threading
import re
from Server import *


class ServerHandler(object):
    def __init__(self, cmd, addr):
        #print("handler has ", cmd)
        self.addr = addr
        self.tCnt = 1
        self.cmd = cmd
    
    def run(self):
        print("handler running with ", self.cmd)
        ##split the incomming cmd
        cmdList = self.cmd.split(" ")
        #print(cmdList)
        ##first string will be the command
        myCmd = cmdList[0]
        ##all other strings will be arguments
        #print("testing cmdList size")
        if len(cmdList) > 1:
            ##turn the cmdList into a comma seperated string
            args = ",".join(cmdList)
        
        try:
            print("reconciling: ", myCmd)
            ##create the attribute to process the command
            func = getattr(self, myCmd)
            
        except AttributeError:
            ##this is to say that there is no attribute youre trying to use
            ##must make a function below
            msg = myCmd + " is not defined!"
            return msg
        
        else:
            ##if there are arguments lets pass them through
            if len(cmdList) > 1:
                #print("getattr with args")
                ##the getattr function can pass strings
                result = func(args)
                
            ##some commands dont require arguments
            else:
                #print("getting result")
                result = func()
            print("result is: ", result)
            
            ##send the result from a function below back to the server
            return result
            
    ##define any function you may need to use anywhere below
    ##you can import other files and use their functions to get values
    ##------------IMPORTANT---------------
    ##----THE SERVER/CLIENT CAN ONLY SEND/RECEIVE STRINGS
    ##----GET YOUR VALUE THEN CONVERT BACK TO STRING

    ##this function show how to get the sending clients information
    ##attempting to use it is futile, just use what inside
    def getMyGameInfo(self):
        for i in globalClients:
            if self.addr.getpeername() == i[0].getpeername():
                return i## retrieve your information
                
    
    def login(self, args):##select a user id
        args = args.split(",")
        uID = args[1]
        print(uID)
        addr = self.addr
        gameID = 0
        playerNum = 0
        inGame = False
        myInfo = [addr, gameID, uID, playerNum, inGame]
        ##remove initial connection info and replace with
        ##player information
        for i in globalClients:
            if i == addr:
                globalClients.remove(i)
        globalClients.append(myInfo)
        msg = str(uID) + " has logged in."
        return msg

    def host(self):## start a game
        ##addr, gameId, uID, playerNum
        for i in globalClients:
            if self.addr.getpeername() == i[0].getpeername():
                if i[1] > 0:
                    msg = "You are already in a game."
                    return msg
                else:
                    mygame = []
                    i[1] = len(games) + 1
                    i[3] = 1
                    mygame.append(i)
                    games.append(mygame)
                    msg = i[2] + " has started a game."
        print("---Current active game ID's---")
        for i in games:
            print(i[0][1])
        return msg
    
    def join(self, args):## join a game
        args = args.split(",")
        gameHost = args[1]
        ## get your information
        for i in globalClients:
            if self.addr.getpeername() == i[0].getpeername():
                myInfo = i
        for i in games:## loop through active games
            if i[0][2] == gameHost:## find the game that matches your host
                myInfo[1] = i[0][1]## set your gameId to that of your hosts
                myInfo[3] = len(i) + 1## set your player number
                i.append(myInfo)## add your info to the hosts game list
                print("Players in the game", i[0][3])
                for j in i:
                    print(j[2], ": player number :", j[3])
        msg = myInfo[2] + " has joined " + gameHost +"'s game."
        return msg

    def leaveGame(self):
        ##print("attempting to leave the game")
        for i in games:
            ##print("looping through games")
            for j in i:
                ##print("looping through players")
                ##print(j[0].getpeername())
                if self.addr.getpeername() == j[0].getpeername():
                    myInfo = j## retrieve your information
                    ##print(myInfo)
                    i.remove(myInfo)
                    ##print("after removal")
                    msg = j[2] + " has left " + str(i[0][2])+"'s game."
                    print(msg)
                    print("Remaining players are:")
                    for j in i:
                        print(j[2])
                    return msg

    def chat(self, args):
        args = args.split(",")
        args = args[1:]
        print("args are ", args)
        chatMsg = ""
        for i in globalClients:
            if self.addr.getpeername() == i[0].getpeername():
                myName = i[2]
        for i in args:
            chatMsg += i + " "
        msg = myName + ": " + chatMsg
        print(msg)
        return msg
        
    def diceRoll(self):
        msg = "DICE CMD"
        print("handling dice")
        return msg


