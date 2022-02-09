import socket
import random
import numpy as np

def startClient(port): 
    ip = "192.168.139.1"
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    clientSocket.connect((ip, port))
    clientSocket.send(numbers.encode())
    stats, _ = clientSocket.recvfrom(1024)
    stats = stats.decode().split(" ")
    print("The sum is", stats[0])
    print("The max is", stats[1])
    print("The average is", stats[2])

numbers = input("Input 5 numbers, seperated by a space: ")
# choose which server to use.
num = random.randint(0,1)
if num % 2 == 0:
    try:
        startClient(8800)
    except:
        startClient(8080)
else:
    try:
        startClient(8080)
    except:
        startClient(8800)