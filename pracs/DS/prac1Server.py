import socket
import numpy as np

def start_server():
    serverPort = 8800
    ip = "192.168.139.1"
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    serverSocket.bind((ip, serverPort))
    serverSocket.listen()
    print("The server is ready to receive")
    while True: 
        client, address = serverSocket.accept()
        numbers = client.recv(1024)
        numbers = numbers.decode().split(" ")
        intnum = np.zeros(5)
        for i in range(5):
            intnum[i] = int(numbers[i])
        stats = ""
        sum = 0
        max = -100000000000000000000
        for i in intnum:
            sum = sum + i
            if i > max:
                max = i
        stats = stats + str(sum)+ " "
        stats = stats + str(max)+ " "
        stats = stats + str(sum/5)+ " "
        client.send(stats.encode())



start_server()
