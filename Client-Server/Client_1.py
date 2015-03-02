from socket import *
from select import *
import sys
import time

logVal = 0
dc = 0

def firstTime():## used to test if its their first connection
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

def send(arg):
    '''
    Game action to send to server
    Use: send(command)
    command = game action
    '''
    # Information of our server to connect to
    HOST = "127.0.0.1"
    PORT = 10205
    BUFFER = 1024
    dc = 0
    
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        #print("Socket is set to server")
        sock.settimeout(1)
    except error:
        print("Failed to open connection with server.")
        return 0 ## you may consider changing this
    start = time.clock()# for timeout
    sock.sendto(arg.encode(), (HOST, PORT))
    print("Sent: ", arg)
    # Client loop
    while(True):
        try:
            data = sock.recvfrom(BUFFER)
            reply = data[0]
            reply = reply.decode()
            print("Received from server: ", reply)#this is where you would send to chat box
            reply1 = data[1]
            print("(Server, IPAddress) ", reply1)
            command = input("\nEnter a command: ")
            if command == "shutdown":
                print("Attempting to shutdown.")
            send(command)
        except error:
            '''
            This will attempt to wait for server reconnection
            by sending the last command given to the server.
            If still no response, it will close the connection attempt.
            '''
            dc += 1
            print("Unable to receive from server!")
            if dc == 10:
                logVal += 1
                if logVal < 2:
                    send(arg)
                else:
                    print("You have disconnected from the server")
                    return 0
        
if __name__ == "__main__":
    command = input("Enter a command: ")
    send(command)
