from socket import *
from select import *
import atexit
import threading
import os
import time

logVal = 0

def firstTime():
    globalUsers = send("getGlobals")
    uID = input("Enter your user name: ")
    if uID not in globalUsers:
        print("User name does not exist.")
        uID = input("Enter a new user ID: ")
        globalUsers.append(uID)
        myID = uID
        return myID
    else:
        myID = uID
        return myID 

def send(command):
    '''
    Game action to send to server
    Use: send(command)
    command = game action
    '''
    # Information of our server to connect to
    HOST = "127.0.0.2"## need to get local address when not in dev
    PORT = 10205
    BUFFER = 1024
    srvCnt = 1
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        #print("Socket is set to server")
        #sock.settimeout(1)
    except error:
        print("Failed to open connection with server.")
        return 0 ## you may consider chaning this
    start = time.clock()# for timeout
    sock.sendto(command.encode(), (HOST, PORT))
    print("Sent: ", command)
    # Client loop
    while(True):
##        try:
        data, addr = sock.recvfrom(BUFFER)
        reply = data.decode()
        #reply = reply.decode()
        print("Received from server: ", reply)#this is where you would send to chat box
        reply1 = addr
        print("(IPAddress, Server Socket) ", reply1)
            #sock.close()
            ##consider returning the send() cmd to the caller
            ## wantedValue = send(cmd)
##            command = input("\nEnter a command: ")
##            if command == 'LOGOUT':
##                print("attempting to logout")
##                sock.close() # stop the connection
##            send(command)
##        except error:
##            if srvCnt <= 4:
##                srvCnt += 1
##                print("Unable to receive from server!   ", error)
##            else:
##                break

        
if __name__ == "__main__":
    cmd = input("Command input: ")
    send(cmd)
    atexit.register(send(leaveGlobals))
##    t = threading.Thread(target=self)
##    print("send intro", t)
##    t.daemon = True
##    t.start()
    
##    while True:
##        if not t.isAlive():
##            os.sys.exit(-1)
##            send(cmd)
##        time.sleep(5)
