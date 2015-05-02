
from Client import *
from time import *

if __name__ == "__main__":
    s = gameClient()
    sleep(.5)
    sendToServer("login david", s)
    sleep(.5)
    sendToServer("join pieter", s)
    sleep(.5)
    sendToServer("chat", s)
    sleep(.5)
    sendToServer("last message", s)
    sleep(.5)
    while True:
        ##input a command to send to server
        cmd = input("enter cmd (type exit to leave): ")
        if cmd == "exit":
            break
        else:
            ##send the command to the server
            sendToServer(cmd, s)
            sleep(.5)##delay for response from server
    s.close()
