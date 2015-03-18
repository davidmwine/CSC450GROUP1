from socket import *

HOST = '127.0.0.1'
PORT = 21567
BUFFER = 1024
ADDR = (HOST, PORT)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)

def send(cmd):
    return cmd
    

def run():
    data = input('> ')
    if not data:
        run()
    sock.send(data.encode())
    while True:
        data = sock.recv(BUFFER)
        if data:
            print(data.decode(), "\n")
    sock.close()

if __name__ == "__main__":
    run()
