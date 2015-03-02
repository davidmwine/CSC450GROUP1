from socket import *
import sys
import socketserver
import threading

# Use these for binding our server
#when ready for WAN testing replace with:
#socket.gethostbyname(socket.gethostname()) ##ip x.x.x.x
HOST = ""
PORT = 10205
clientsList = []
tCnt = 1 # thread count

#this class will make a thread
#still trying to expand this to obtain all relevant player information
class MyThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print("doing stuff")
    

## Create the server
server = socket(AF_INET, SOCK_DGRAM)
server.bind((HOST, PORT))

def newThread(thread):
    if thread not in clientsList:
        clientsList.append(thread)
    else:
        thread = MyThread()
        newthread(thread)

#always on listener, listening for commands from player/client
while(True):
    message, address = server.recvfrom(1024)
    print("\nReceiving from client: ", message.decode())

    #split each send word into a list - to be used with handler
    cmdList = message.split()

    if len(cmdList) > 1:
        for i in cmdList:
            print(i)        
##      if you need to send an argument with a command
##      create a handler program

    #make a new thread
    if message.decode() == "thread":
        worker = threading.Thread()
        worker.daemon = True
        worker.start()#starts in MyThread
        print("Starting thread ", worker)
        clientsList.append(worker)

    #close the last thread in the list - modify to be specific thread
    if message.decode() == "close":
        if len(clientsList) > 0:
            lastThread = clientsList.pop(-1)
            print("Closing ", lastThread)
            lastThread._stop()
            print("stopped")

    #stop theserver
    if message.decode() == "shutdown":
        print("You received the shutdown command.")
        server.sendto(message.upper(), address)
        sys.exit()

    #list all active threads
    if message.decode() == "active":
##        mainThreads = threading.enumerate()
##        print(mainThreads)
        for i in range(len(clientsList)):
            print(clientsList[i].getName(), clientsList[i])

    server.sendto(message.upper(), address)## this returns the command back to the client
