import time
import socket
import sys
import threading
import os

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
    # closes a connection and adds to the log file.
    connectedClients.remove(client)
    client.close()
    # tell all other users
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

def receive(client, logFile):
    # receive messages from the client
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

def serverCrash(logFile, crash):
    # crashes the server
    # write to the log file
    if logFile.closed:
            logFile = open('server.log', 'a')
    if crash:
        logFile.write('Server crashed\n')
    else:
        logFile.write('Server closed\n')
    clients = connectedClients.copy()
    # close all connections
    for client in clients:
        connectedClients.remove(client)
        client.close()
        username = usernames[client]
        nicknames.remove(username)
        message = f'{username} left!'
        del usernames[client]
        #write to file
        logFile.write(message+'\n')
    logFile.close()
    if crash:
        print('Server crashed')
    os._exit(0)

def serverWrite(logFile):
    # allows an input the server - used to close the server
    try:
        while 1:
            try:
                message = input('')
                if message == 'exit':
                    serverCrash(logFile, True)
                elif message == 'q':
                    serverCrash(logFile, False)
            except:
                serverCrash(logFile, True)
    except KeyboardInterrupt:
        serverCrash(logFile, True)


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
            # add the client and usernames
            usernames[client] = username
            nicknames.append(username)
            connectedClients.append(client)
            if len(connectedClients) == 1:
                logFile = open('server.log', 'a') #adds to end of file
            message = f'{username} joined at {str(address)}'
            print(message)
            logFile.write(message+'\n')
            broadcast("{} joined!".format(username).encode())
            client.send(f'Welcome to the server {username}! Enter your messages below where there is a >. Type exit to exit the chat.\n'.encode())
            #starts the threads
            receiveThread = threading.Thread(target=receive, args=(client,logFile))
            writeThread = threading.Thread(target=serverWrite, args=(logFile,))
            receiveThread.start()
            writeThread.start()

def writeToLog():
    # write to the log file
    logFile = open('server.log','w') #creates file or overwrites existing file
    logFile.write(f'Listening at {ip}:{port}\n')
    logFile.close()

ip = ''
port = getParameters()
# create socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
serverSocket.bind((ip, port))
serverSocket.listen()
print(f'Listening at {ip}:{port}')
writeToLog()
connectedClients = []
nicknames = []
usernames = {}
print("Type q to exit the server. Type exit to crash.")
receiveConnection()
