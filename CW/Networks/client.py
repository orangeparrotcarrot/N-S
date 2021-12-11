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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect((ip,port))
        clientSocket.setblocking(False)
        print(f"You entered the chat. Your username is {user}. To leave the chat, press q.")
        while True:
            socketList = [clientSocket]
            # print(socketList)
            # not working??
            # r, w, e = select.select(socketList, [],socketList)
            read_sockets, write_sockets, error_sockets = select.select(socketList , [], [])
            print(read_sockets)
            for sock in socketList:
                if sock == clientSocket:
                    clientSocket.sendall(user.encode())
                    data = sock.recv(1024)
                    # clientSocket.sendall(user.encode())
                    if (not data) or (data.decode == 'q'):
                    # if data.decode == 'q':
                        print("Disconnected from chat server")
                        sys.exit()
                    else:
                        print('>',data.decode())
                else:
                    message = input(f'{user}: ')
                    dataToSend = f'{user}: {message}'
                    clientSocket.sendall(dataToSend.encode())
                



        # data = clientSocket.recv(1024)
        # # print('data received: ',data)
        # print(data)

        #to leave the chat.
        # if message == 'q':
        #     break
    #     try:
    #         receivedmessage = clientSocket.recv(1024).decode('utf-8')
    #         continue
    #     except:
    #         continue


# if __name__ == "__main__":
ip, user, port = getParameters()
startClient()
print('You have left the chat')
