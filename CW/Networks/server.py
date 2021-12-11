import socket
import select
import sys

def getparameters():
    try: 
        port = sys.argv[1]
        port = int(port)
        return port
    except:
        print("Port number must be an integer")
        sys.exit()

def broadcast(sock, message):
    # print(len(socketList))
    for socket in socketList:
        # send the message only to peer
        # if socket != serverSocket and socket != sock : #ie all other clients
        if socket != serverSocket:
            try :
                socket.sendall(message.encode())
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in socketList:
                    socketList.remove(socket)
    print(message)

def startServer(port):
    clients = {}
    while True:
        r, w, e = select.select(socketList, [],socketList)
        # print(r)
        # print(socketList)
        # print("\n")
        for sock in r:
        #if it is a new connection - tell everyone they joined
            if sock == serverSocket:
                # new client - accept connection
                connection, clientAddress = serverSocket.accept()
                socketList.append(connection)
                data = connection.recv(1024)
                x = data.decode()
                clients[x] = connection
                # print('client connected at', connection)
                # broadcastMessage(f'{x} has entered the chat', connection)
                broadcast(connection, f'{x} has entered the chat. Say hi!')
    #             # with connection:
    #             #     while True:
    #             #         data = connection.recv(1024)
    #             #         x = data.decode()
    #             #         print(x)
    #             #         if not data:
    #             #             break
    #             #         elif x == 'q':
    #             #             break
    #             #         connection.sendall(data)
    #             # break   
        # if it is an old connection - allow them to send messages
            # else:
            #     with sock:
            #         while 1:
            #             data = sock.recv(1024)
            #             x = data.decode()
            #             if not data:
            #                 break
            #             if x == 'q':
            #                 broadcastMessage('Someone has left the chat', sock)
            #                 serverSocket.remove(sock)
            #                 sys.exit()
            #             sock.sendall(data)
            # if len(socketList) == 1:
            #     sys.exit()
                # break

# single person !!

    # while True:
    #     conn, addr = serverSocket.accept()
    #     with conn:
    #         while True:
    #             #basically gets data, and sends it back
    #             data = conn.recv(1024)
    #             x = data.decode()
    #             print(x)
    #             if not data:
    #                 break
    #             elif x == 'q':
    #                 # if the user ends the chat
    #                 break
    #             # conn.sendall(data)
    #     break

# cd desktop/du/year 2/networks and systems/cw/networks

port = getparameters()
ip = '192.168.139.1'
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverSocket.bind((ip,port))
    serverSocket.listen()
    print(f'Listening for connections on {ip}:{port}')

    clients = {}
    socketList = [serverSocket]

    startServer(port)
