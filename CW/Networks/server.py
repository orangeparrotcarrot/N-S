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

def broadcast(message):
    #sends a message to each client
    for client in connectedClients:
        client.send(message)

def handle(client, logFile):
    while 1:
        try:
            message = client.recv(1024)
            broadcast(message)
            message = message.decode()
            print(message)
            logFile.write(message+'\n')
        except:     #if something goes wrong   
            #close the connection                      
            connectedClients.remove(client)
            client.close()
            #tell all other users
            nickname = usernames[client]
            message = f'{nickname} left!'
            broadcast(message.encode())
            print(message)
            del usernames[client]
            #write to file
            logFile.write(message+'\n')
            if len(connectedClients)==0:
                logFile.close()
            break

def receiveConnection():
    #accepts multiple clients
    while 1:
        if len(connectedClients)==0:
            logFile = open('server.log', 'a')
            print('log open')
        client, address = serverSocket.accept() 
        client.send('USERNAME'.encode())
        nickname = client.recv(1024).decode()
        usernames[client] = nickname
        connectedClients.append(client)
        print(f'{nickname} joined at {str(address)}')
        logFile.write(f'{nickname} joined at {str(address)}\n')
        broadcast("{} joined!".format(nickname).encode())
        client.send(f'Welcome to the server {nickname}!'.encode())
        receiveThread = threading.Thread(target=handle, args=(client,logFile))
        receiveThread.start()

def writeToLog():
    logFile = open('server.log','w')
    logFile.write(f'Listening at {ip}:{port}\n')
    logFile.close()

ip = '192.168.139.1'
port = getParameters()
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
serverSocket.bind((ip, port))
serverSocket.listen()
print(f'Listening at {ip}:{port}')
writeToLog()
connectedClients = []
usernames = {}
receiveConnection()
# cd desktop/du/year 2/networks and systems/cw/networks
# server.py 8080
