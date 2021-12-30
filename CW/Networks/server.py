import socket
import sys
import threading

def getParameters():
    try: 
        port = sys.argv[1]
        port = int(port)
        return port
    except:
        print("Port number must be an integer")
        sys.exit()                                      

def broadcast(message):                                                 #broadcast function declaration
    for client in clients:
        client.send(message)

def handle(client):                                         
    while True:
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)
            broadcast(message)
            print(message.decode())
        except:                               
            clients.remove(client)
            client.close()
            nickname = nicknames[client]
            del nicknames[client]
            broadcast('{} left!'.format(nickname).encode())
            print(f'{nickname} left!')
            break

def receiveConnection():                                                          #accepting multiple clients
    while True:
        client, address = serverSocket.accept() 
        client.send('NICKNAME'.encode())
        nickname = client.recv(1024).decode()
        nicknames[client] = nickname
        clients.append(client)
        print(f'{nickname} joined at {str(address)}')
        broadcast("{} joined!".format(nickname).encode())
        client.send('Connected to server!'.encode())
        receiveThread = threading.Thread(target=handle, args=(client,))
        receiveThread.start()


ip = '192.168.139.1'                                                      #LocalHost
port = getParameters()                                                             #Choosing unreserved port

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
serverSocket.bind((ip, port))                                               #binding host and port to socket
serverSocket.listen()
print(f'Listening at {ip}:{port}')

clients = []
nicknames = {}
receiveConnection()

# cd desktop/du/year 2/networks and systems/cw/networks
