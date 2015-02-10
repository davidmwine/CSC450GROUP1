import sockets
from sys import *
import time
from math import *

def connect_loop():##if unable to connect ask user try again
    ask = input("Try again (y/n)?")
    if ask == 'y' or ask == 'N':
        client()
    else if ask == 'n' or ask == 'N':
        return 0
    else:
        print("Invalid response!")
        connect_loop()

def dcLoop():## loop for reestablishing connection
    


def sendToServer(*args):
    UDP_IP = socket.gethostbyname(socket.gethostname()) ##ip x.x.x.x
    UDP_PORT = 50134 #set a known empty socket
    BUFFER = 1024 ##bytes to buffer for - more than enough
    
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        
    except socket.error:
        print("Unable to connect!")
        connect_loop()
        return 0# not sure if i should have this here, resolved in connect loop()
    
    s.close()
            
    
##handler design
def handler(*args):
    data = args.split()
    command = data[0]
    cmdArgs = data[1, -1]
    print(command)
    print(cmdArgs)
    
    
