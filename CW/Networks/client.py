import socket
import sys
import threading

def getParameters():
    #gets the ip address, user nickname and port number from the command line.
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
    if user == '':
        print('Please enter a username')
        sys.exit()
    return ip, user, port

def receiveMessage():
    #receive a message
    while 1:
        try:
            message = clientSocket.recv(1024).decode()
            if message == 'USERNAME':
                clientSocket.sendall(user.encode())
            else:
                print(message)
        except:
            print("An error occured!")
            clientSocket.close()
            break

def writeMessage():
    #send a message
    while 1:
        message = input('')
        message = f'{user}: {message}'
        clientSocket.sendall(message.encode())


ip, user, port = getParameters()
try:
    #try and connect to the server
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
    clientSocket.connect((ip, port))
    receive_thread = threading.Thread(target=receiveMessage)               #receiving multiple messages
    receive_thread.start()
    write_thread = threading.Thread(target=writeMessage)                   #sending messages 
    write_thread.start()
except:
    #if something is wrong.
    print('Server may be unavailable or the IP address / port number is incorrect. \nCheck IP address and host and try again later')
    sys.exit()

# cd desktop/du/year 2/networks and systems/cw/networks
# client.py 192.168.139.1 liv 8080