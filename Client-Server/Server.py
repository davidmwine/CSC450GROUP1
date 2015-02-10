import socket, sys, select, threading

class Server:
    def __init__(self):
        self.host = ''##ipaddress of the server remains blank
        self.port = 22002##unused port
        self.backlog = 6## not sure we can do 6, max on most systems is 5
        self.size = 1024 ## this is the buffer size from Client
        self.server = None## initiate a server variable
        self.threads = []##list for user ipaddresses

    def open_socket(self):
        '''Individual socket creation for each user'''
        try:
            self.server = socket(AF_INET, SOCK_STREAM)##debug this, check the sources
            self.server.bind((self.host, self.port))
            self.server.listen(backlog)
        except socket.error:
            if self.server:
                self.server.close()## unable to open the socket
            sys.exit(1)
            
    def run(self):
        '''Adds the user to the current connection'''
        self.open_socket()
        readin = [self.server,sys.stdin] 
        running = 1 
        while running:
            inputready,outputready,exceptready = select.select(readin,[],[]) 

            for s in inputready: 

                if s == self.server:
                    # handle the server socket 
                    c = Client(self.server.accept()) 
                    c.start() 
                    self.threads.append(c) 

                elif s == sys.stdin: 
                    # handle standard input 
                    junk = sys.stdin.readline() 
                    running = 0 

        # close all threads, server waits to disconnect until all users exit 
        self.server.close() 
        for c in self.threads: 
            c.join()
########################################################
class Client(threading.Thread): 
    def __init__(self,client,address): 
        threading.Thread.__init__(self) 
        self.client = client 
        self.address = address 
        self.size = 1024 

    def run(self): 
        running = 1 
        while running: 
            data = self.client.recv(self.size) 
            if data: 
                self.client.send(data) 
            else: 
                self.client.close() 
                running = 0 

if __name__ == "__main__": 
    s = Server() 
    s.run()
