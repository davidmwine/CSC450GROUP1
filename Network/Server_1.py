from socket import *
import socketserver
import threading
from ServerHandler import *

# Use these for binding our server
#when ready for WAN testing replace with:
#socket.gethostbyname(socket.gethostname()) ##ip x.x.x.x
HOST = "127.0.0.1"
PORT = 10205
clientsList = []
tCnt = 1
cmd = ""
handle = ServerHandler(cmd)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("Starting ", self.name, ". With ID ", self.threadID, ". And counter of ", self.counter)    

## Create the server
server = socket(AF_INET, SOCK_DGRAM)
server.bind((HOST, PORT))

##def startThread(self):
##    self.thread_listener.start()

while(True):
    message, address = server.recvfrom(1024)
    clientsList.append([message, address, []])
    print("Receiving from client: ", message.decode())
    handle = ServerHandler(message.decode())
    
    
    if message.decode() == "thread":
        print("You received the thread command.")
        name = "thread " + str(tCnt)
        thread = myThread(1, name, tCnt)
        print(thread.name, "now open.")
        tCnt += 1
        
    if message.decode() == "shutdown":
        print("You received the shutdown command.")
        server.shutdown()
    
    if message == "getGlobals":
        message = [getGlobals, globalUsers]
        server.sendto(globalUsers, address)

    server.sendto(message.upper(), address)## this returns the command back to the client
