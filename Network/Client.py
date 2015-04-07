from select import *
from socket import *
import sys
import threading
from queue import *

msg = ""
uID = "User-1"
cmdList = Queue(maxsize = 0)

def gameClient():
    HOST = "127.0.0.1"## need to get local address when not in dev
    PORT = 10205
    BUFFER = 2048
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(2)
    
    try:
        s.connect((HOST, PORT))
        print("Connected to server")
    except:
        print("Failed to open connection with server.")
        sys.exit()
    print("You are now connected to the server.")

    ######################################
    ## Create a thread for sending and receiving data
    ## This is critical 
    ######################################
    t = threading.Thread(target = sendToServer, args = (msg, s))
    t.daemon = True
    t.start()
    print("\nSend thread has started!!\n")
    
    r = threading.Thread(target = receiveFromServer, args = (s,BUFFER,))
    r.daemon = True
    r.start()
    print("\nReceive thread has started!!\n")
    
    ######################################
    ##Test that your threads work - consider this for initial logon userID
    ######################################
    ##sendToServer(uID, s)
    ##receiveFromServer(s, BUFFER)
    ######################################
    return s

def receiveFromServer(s, BUFFER):
    print("In receive thread.")
    while True:
        try:
            #print("Trying to receive.")
            data = s.recv(BUFFER)
            cmdList.put(data.decode())
            print("\nReceiving: %s" % data.decode())
        except:
            ## continue to always be listening
            pass

def sendToServer(msg, s):
    #print("In send thread.")
    try:
        if len(msg) > 0:
            s.send(msg.encode())
            print("\nSent: %s" % msg)
    except:
        pass

if __name__ == "__main__":
    gameClient()
