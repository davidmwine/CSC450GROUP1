from socket import *

HOST = 'localhost'
PORT = 21567
BUFFER = 1024
ADDR = (HOST, PORT)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)

def send(cmd):
    return cmd
    

def run():
    while True:
        data = input('> ')
        if not data:
                run()
            
        sock.send(data.encode())
        data = sock.recv(BUFFER)
        if not data:break
        print(data.decode('utf-8'))
    sock.close()

if __name__ == "__main__":
    run()
