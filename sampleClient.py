
from Client import *
from time import *

if __name__ == "__main__":
    s = gameClient()
    sleep(.5)
    sendToServer("login pieter", s)
    sleep(.5)
    sendToServer("host", s)
    sleep(.5)
    sendToServer("chat OMG im finally chatting", s)
    sleep(2)
    sendToServer("chat you are chatting", s)
    sleep(1)
    sendToServer("chat lets ge tinto the game", s)
    sleep(.2)
    sendToServer("chat finishing chat", s)
    sleep(.2)
    sendToServer("chat message", s)
    sleep(.5)
##    while True:
##        ##input a command to send to server
##        cmd = input("enter cmd (type exit to leave): ")
##        if cmd == "exit":
##            break
##        else:
##            ##send the command to the server
##            sendToServer(cmd, s)
##            sleep(.5)##delay for response from server
##     s.close()
