import socket
import sys
import threading

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

def receiveMessage():
    while True:                                                 #making valid connection
        try:
            message = clientSocket.recv(1024).decode()
            if message == 'NICKNAME':
                clientSocket.sendall(user.encode())
            else:
                print(message)
        except:                                                 #case on wrong ip/port details
            print("An error occured!")
            clientSocket.close()
            break

def writeMessage():
    while True:                                          #message layout
        message = '{}: {}'.format(user, input(''))
        clientSocket.sendall(message.encode())

ip, user, port = getParameters()

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
clientSocket.connect((ip, port))                             #connecting client to server
print(f'Welcome to the server {user}!')
receive_thread = threading.Thread(target=receiveMessage)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=writeMessage)                   #sending messages 
write_thread.start()