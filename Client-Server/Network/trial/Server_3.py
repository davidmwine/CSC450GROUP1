import socket
import sys
import os
import threading
import time
#import traceback
from itertools import cycle
 
MAX_INDEX = 100                      # The max of cyclic index
MAX_LEN = 10                         # Message queue length
host = 'localhost'                            # Bind to all interfaces
port = 50000
 
def mesg_index(old, last, new):
    """
    This computes the index value of the message queue from where the reader
    should return messages.  It accounts for having a cyclic counter.
    This code is a little tricky because it has to catch all possible
    combinations.
    old -> index of oldest (first) message in queue
    last -> index of last message read by the client thread
    new -> index of newest (last) message in the queue
    """
    if new >= old:
        # normal case
        if last >= old and last < new:
            return (last - old + 1)
        else:
            return 0
    else:
        # cyclic roll over (new < old)
        if last >= old:
            return (last - old + 1)
        elif last < new:
            return (MAX_INDEX - old + last)
        else:
            return 0

class MSGQueue(object):
    """
    Manage a queue of messages for Chat, the threads will read and write to
    this object.  This is an implementation of the readers - writers problem
    with a bounded buffer.
    """
    def __init__(self):
        self.msg = []
        self.cyclic_count = cycle(range(MAX_INDEX))
        self.current = -1
        self.readers = 0
        self.writers = 0
        self.mutex1 = threading.Lock()
        self.mutex2 = threading.Lock()
        self.readPending = threading.Lock()
        self.writeBlock = threading.Lock()
        self.readBlock = threading.Lock() 

    def reader(self, lastread):
        self.readPending.acquire()
        self.readBlock.acquire()
        self.mutex1.acquire()
        self.readers = self.readers + 1
        if self.readers == 1:
            self.writeBlock.acquire()
            
        self.mutex1.release()
        self.readBlock.release()
        self.readPending.release()
        
        # here is the critical section
        if lastread == self.current: # or not len(self.msg):
            retVal = None
        else:
            MsgIndex = mesg_index(self.msg[0][0], lastread, self.current)
            retVal = self.msg[MsgIndex:]
        # End of critical section
        
        self.mutex1.acquire()
        self.readers = self.readers - 1
        
        if self.readers == 0:
            self.writeBlock.release()
            
        self.mutex1.release()
        return retVal
 
    def writer(self, data):
        self.mutex2.acquire()
        self.writers = self.writers + 1
        
        if self.writers == 1:
            self.readBlock.acquire()
            
        self.mutex2.release()
        self.writeBlock.acquire()
        
        # here is the critical section
        self.current = self.cyclic_count.next()
        self.msg.append((self.current, time.localtime(), data))
        while len(self.msg) > MAX_LEN:
            del self.msg[0]     # remove oldest item

        # End of critical section
        
        self.writeBlock.release()
        self.mutex2.acquire()
        self.writers = self.writers - 1
        
        if self.writers == 0:
            self.readBlock.release()
            
        self.mutex2.release()

def sendAll(sock, lastread):
    # this function just cuts down on some code duplication
    global chatQueue
    reading = chatQueue.reader(lastread)
    
    if reading == None:
        return lastread
    
    for (last, timeStmp, msg) in reading:
        sock.send("At %s -- %s" % (time.asctime(timeStmp), msg))
    return last
 
def clientExit(sock, peer, error=None):
    # this function just cuts down on some code duplication
    global chatQueue
    print("A disconnect by ", peer)
    if error:
        msg = peer + " has exited -- " + error + "\r\n"
    else:
        msg = peer + " has exited\r\n"
    chatQueue.writer(msg) 

def handlechild(clientsock):
    # Do the sending and receiving of data for one client
    global chatQueue
    # lastreads of -1 gets all available messages on first read, even
    # if message index cycled back to zero.
    lastread = -1
    # the identity of each user is called peer - they are the peer on the other
    # end of the socket connection.
    peer = clientsock.getpeername()
    print("Got connection from ", peer)
    msg = str(peer) + " has joined\r\n"
    chatQueue.writer(msg)

    while 1:
        # check for and send any new messages
        lastread = sendAll(clientsock, lastread)
        try:
            data = clientsock.recv(4096)
        except socket.timeout:
            continue
        except socket.error:
            # caused by main thread doing a socket.close on this socket
            # It is a race condition if this exception is raised or not.
            print("Server shutdown")
            return
        except:  # some error or connection reset by peer
            clientExit(clientsock, str(peer))
            break
        if not len(data): # a disconnect (socket.close() by client)
            clientExit(clientsock, str(peer))
            break

        # Process the message received from the client
        # First check if it is a one of the special chat protocol messages.
        if data.startswith('/nick'):
            oldpeer = peer
            peer = data.replace('/nick', '', 1).strip()
            if len(peer):
                chatQueue.writer("%s now goes by %s\r\n" \
                                % (str(oldpeer), str(peer)))
            else: peer = oldpeer

        elif data.startswith('/quit'):
            bye = data.replace('/quit', '', 1).strip()
            if len(bye):
                msg = "%s is leaving now -- %s\r\n" % (str(peer), bye)
            else:
                msg = "%s is leaving now\r\n" % (str(peer))
            chatQueue.writer(msg)
            break            # exit the loop to disconnect
        else:
            # Not a special command, but a chat message
            chatQueue.writer("Message from %s:\r\n\t%s\r\n" % (str(peer), data))

    #-- End looping for messages from/to the client
    # Close the connection
    clientsock.close()
 
# Begin the main part of the program
if __name__ == '__main__':
    # One global message queue, which uses the readers and writers
    # synchronization algorithm.
    chatQueue = MSGQueue()
    clients = []

    # Set up the socket.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(3)

    while 1:
        print("Waiting for Connections...")
        try:
            clientsock, clientaddr = s.accept()
            # set a timeout so it won't block forever on socket.recv().
            # Clients that are not doing anything check for new messages
            # after each timeout.
            clientsock.settimeout(1)
        except KeyboardInterrupt:
            # shutdown - force the threads to close by closing their socket
            s.close()
            for sock in clients:
                sock.close()
            break
        #except:
        #    traceback.print_exc()
        #    continue
        clients.append(clientsock)
        t = threading.Thread(target = handlechild, args = [clientsock])
        t.setDaemon(1)
        t.start()
