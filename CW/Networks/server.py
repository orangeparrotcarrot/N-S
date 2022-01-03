import socket
import sys
import threading

def getParameters():
    #gets port number from command line
    try: 
        port = sys.argv[1]
        port = int(port)
        return port
    except:
        print("Port number must be an integer")
        sys.exit()                                      

def broadcast(message, currentClient):
    #sends a message to each client
    for client in clients:
        client.send(message)

def handle(client):
    #handles the clients
    while 1:
        try:
            #receive a valid message from a client
            message = client.recv(1024)
            broadcast(message, client)
            print(message.decode())
            logFile.write(message.decode())
            print(logFile.closed)
        except:
            #if the message is invalid, or something goes wrong.
            clients.remove(client)
            client.close()
            nickname = usernames[client]
            del usernames[client]
            broadcast('{} left!'.format(nickname).encode(),'')
            print(f'{nickname} left!')
            logFile.write(f'{nickname} left\n')
            break

def write():
    while 1:
        try:
            message = input('')
            if message == 'q':
                print(message)
        except KeyboardInterrupt:
            print('keyboard interrupt')
        #     logFile.close()
        #     serverSocket.close()
        #     print(logFile.closed)
        #     print('server closed')
        #     sys.exit() #won't work

def receiveConnection():
    #accepts multiple clients
    while 1:
        try:
            client, address = serverSocket.accept() 
            # receives nickname from client
            client.send('USERNAME'.encode())
            nickname = client.recv(1024).decode()
            usernames[client] = nickname
            clients.append(client)
            print(f'{nickname} joined at {str(address)}')
            logFile.write(f'{nickname} joined at {str(address)}\n')
            print(logFile.closed)
            broadcast("{} joined!".format(nickname).encode(),client)
            client.send(f'Welcome to the server {nickname}!'.encode())
            receiveThread = threading.Thread(target=handle, args=(client,))
            receiveThread.start()
            writeThread = threading.Thread(target=write)
            writeThread.start()
        except KeyboardInterrupt:
            print('interrupt')
            break


ip = '192.168.139.1'
port = getParameters()
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
serverSocket.bind((ip, port))
serverSocket.listen()
print(f'Listening at {ip}:{port}')
with open('server.log', 'w+') as logFile:
# logFile = open('server.log','w')
    logFile.write(f'Listening at {ip}:{port}\n')
    # logFile.close()
    clients = []
    usernames = {}
    receiveConnection()
# cd desktop/du/year 2/networks and systems/cw/networks
# server.py 8080
