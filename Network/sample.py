'''
Use this to see a sample send command
I still need to expand to allow multiple args
'''

from Client_1_user0 import *
from ServerHandler import *



def run():
    cmd = input("Enter Command:")
    send(cmd)
    run()
        
if __name__ == "__main__":
    run()
