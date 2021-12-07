import socket

def start_client():
    serverName = "192.168.139.1"
    serverPort = 8800
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        message = input("Input lowercase sentence: ")
        print("client, ", message)
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        if message == 'q':
            clientSocket.close()
            break
        print(modifiedMessage.decode())

if __name__ == "__main__":
    start_client()
