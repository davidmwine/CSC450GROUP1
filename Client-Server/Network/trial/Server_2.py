import socket
import threading

globalClients = []

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = clientsocket
        print("[+] New thread started for ", ip, ":",str(port))
        addr = (ip, port)
        globalClients.append(self.socket)

    def run(self):
        data = "any"
        while len(data):
            try:
                data = self.socket.recv(2048)
            except:
                continue
            #handle data here
            print("Client ('%s', %s) sent : %s"%(self.ip, str(self.port), data))
            data = "Receiving from server : " + data.decode()
            for i in globalClients:
                try:
                    i.send(data.upper().encode())
                except:
                    globalClients.remove(i)

        print("[-] Client at ",self.ip," disconnected...")

host = "localhost"
port = 21567

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))
tcpsock.listen(4)
print("Listening for incoming connections...")

while True:
    #pass clientsock to the ClientThread thread object being created
    (clientsock, (ip, port)) = tcpsock.accept()
    if clientsock not in globalClients:
        newthread = ClientThread(ip, port, clientsock)
        newthread.start()
