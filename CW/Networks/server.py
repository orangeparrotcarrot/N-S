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
    #doesn't send to correct clients
    # print(message)
    eligibleSockets = socketList.copy()
    # print(eligibleSockets)
    try:
        eligibleSockets.remove(sock)
    except:
        print('sock didn\'t work')
    try:
        eligibleSockets.remove(serverSocket)
    except:
        print('server did not work')
    # print(eligibleSockets)
    for socket in eligibleSockets:
        # send the message only to peer
        if (socket != serverSocket) and (socket != sock) : #ie all other clients
        # if socket != serverSocket:
            try :
                socket.sendall(message.encode())
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in socketList:
                    socketList.remove(socket)
    # print(message)

def startServer(port):
    i = 0
    while True:
        r, w, e = select.select(socketList, [],socketList)
        if (serverSocket in r):
                connection, clientAddress = serverSocket.accept()
                socketList.append(connection)
                data = connection.recv(1024)
                x = data.decode()
                clients[connection]=x
                connection.sendall(f"You entered the chat. Your username is {x}. To leave the chat, press q.".encode())
                broadcast(connection, f'{x} has entered the chat. Say hi!')
                # serverSocket.sendall(f"You entered the chat. Your username is {x}. To leave the chat, press q.".encode())
        else:
            for s in r:
                user = clients[s]
                data = s.recv(1024)
                x=data.decode()
                message = x.split()
                print(message)
                if (not data) or (message[1]=='q'):
                    s.sendall('q'.encode())
                    broadcast(connection, f'{user} has left the chat')
                    socketList.remove(s)
                    del clients[s]
                    connection.close()
                else:
                    broadcast(connection, x)
        # print(socketList)
        # print("\n")
       

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
# client.py 192.168.139.1 x 8080

port = getparameters()
ip = '192.168.139.1'
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverSocket.bind((ip,port))
    serverSocket.listen()
    print(f'Listening for connections on {ip}:{port}')

    clients = {}
    socketList = [serverSocket]

    startServer(port)
