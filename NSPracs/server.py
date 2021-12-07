import socket
# import threading

def start_server():
    serverPort = 8800
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    serverSocket.bind(('192.168.139.1', serverPort))
    print("The server is ready to receive")
    while True: 
        message, clientAddress = serverSocket.recvfrom(1024)
        # modifiedMessage = message.decode()
        print(message.decode())
        if message.decode() == 'q':
            break
        else:
            serverSocket.sendto(message.upper(), clientAddress)


if __name__=="__main__":
    start_server()
