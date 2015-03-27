
from Client import *
from time import *

if __name__ == "__main__":
    s = gameClient()
    msg = input("Attempt to send: ")
    sendToServer(msg, s)
    sleep(.5)
    sendToServer("msg 1", s)
    sleep(.5)
    sendToServer("msg 2", s)
    sleep(.5)
    sendToServer("msg 3", s)
    sleep(.5)
    sendToServer("last message", s)
    sleep(.5)
