import socket
import select
import sys

def getParameters():
    try:
        ip = sys.argv[1]
        user = sys.argv[2]
        port = sys.argv[3]
    except:
        print("Format: IP address username port number")
        sys.exit()
    try:
        port = int(port)
    except:
        print("Port number (third input) must be an integer")
        sys.exit()
    return ip, user, port

def startClient():
    #doesn't work - has to send a message to receive a message
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect((ip,port))
        # clientSocket.setblocking(False)
        # print(f"You entered the chat. Your username is {user}. To leave the chat, press q.")
        clientSocket.sendall(user.encode())
        data = clientSocket.recv(1024)
        print(data.decode())
        while True:
            message = input(f'{user}: ')
            if message != '':
                dataToSend = f'{user}: {message}'
                clientSocket.sendall(dataToSend.encode())
                data = clientSocket.recv(1024)
                x = data.decode()
                print(x)
                if x == 'q':
                    print(x)
                    clientSocket.close()
                    print('closed')
                    sys.exit()
                

# if __name__ == "__main__":
ip, user, port = getParameters()
startClient()
print('You have left the chat')
