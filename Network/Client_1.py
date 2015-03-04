from socket import *
from select import *
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
    HOST = "127.0.0.1"
    PORT = 10205
    BUFFER = 1024
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        #print("Socket is set to server")
        sock.settimeout(1)
    except error:
        print("Failed to open connection with server.")
        return 0 ## you may consider chaning this
    start = time.clock()# for timeout
    sock.sendto(command.encode(), (HOST, PORT))
    print("Sent: ", command)
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
            if command == 'LOGOUT':
                print("attempting to logout")
                sock.close() # stop the connection
            send(command)
        except error:
            print("Unable to receive from server!")

        
if __name__ == "__main__":
    command = input("Enter a command: ")
    send(command)
