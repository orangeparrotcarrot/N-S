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

def broadcastMessage(message, client):
    print('message:', message)
    print(socketList)
    for c in socketList:
        if (c != serverSocket):
            try:
                print(":)")
                c.sendall(message) #not working???
                print('message sent')
            except:
                print(':(')
                c.close()
                # broadcastMessage(f'{c} has left the chat', c)
                socketList.remove(c)
                print('connection closed')

def startServer(port):
    while True:
        r, w, e = select.select(socketList, [],socketList)
        for sock in r:
        #if it is a new connection - tell everyone they joined
            if sock == serverSocket:
                # new client - accept connection
                connection, clientAddress = serverSocket.accept()
                socketList.append(connection)
                broadcastMessage('Someone has entered the chat', connection)
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
            else:
                with sock:
                    while 1:
                        data = sock.recv(1024)
                        x = data.decode()
                        if not data:
                            break
                        if x == 'q':
                            broadcastMessage('Someone has left the chat', sock)
                            serverSocket.remove(sock)
                            sys.exit()
                        sock.sendall(data)
            if len(socketList) == 1:
                sys.exit()
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
