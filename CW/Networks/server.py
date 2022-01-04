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
        client.sendall(message)

def closeConnection(client,logFile):
    connectedClients.remove(client)
    client.close()
    #tell all other users
    username = usernames[client]
    nicknames.remove(username)
    message = f'{username} left!'
    broadcast(message.encode())
    print(message)
    del usernames[client]
    #write to file
    logFile.write(message+'\n')
    if len(connectedClients)==0:
        logFile.close()

def handle(client, logFile):
    while 1:
        try:
            #receive message, and send to other clients
            message = client.recv(1024)
            broadcast(message)
            message = message.decode()
            #print message and write to file
            print(message)
            logFile.write(message+'\n')
        except:     #if something goes wrong   
            #close the connection                  
            closeConnection(client,logFile)
            break

def receiveConnection():
    #accepts multiple clients
    while 1:
        client, address = serverSocket.accept() 
        #get username from client
        client.send('USERNAME'.encode())
        username = client.recv(1024).decode()
        if username in nicknames:
            client.send('USERNAME TAKEN'.encode())
        else:
            usernames[client] = username
            nicknames.append(username)
            connectedClients.append(client)
            if len(connectedClients)==1:
                logFile = open('server.log', 'a') #adds to end of file
            print(f'{username} joined at {str(address)}')
            print((connectedClients))
            logFile.write(f'{username} joined at {str(address)}\n')
            broadcast("{} joined!".format(username).encode())
            client.send(f'Welcome to the server {username}! Enter your messages below on the blank line. Type exit to exit the chat.'.encode())
            #starts the thread
            receiveThread = threading.Thread(target=handle, args=(client,logFile))
            receiveThread.start()

def writeToLog():
    logFile = open('server.log','w') #creates file or overwrites existing file
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
nicknames = []
usernames = {}
receiveConnection()
# cd desktop/du/year 2/networks and systems/cw/networks
# server.py 8080
