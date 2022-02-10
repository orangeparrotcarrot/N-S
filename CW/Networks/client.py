import socket
import sys
import threading
import os

def getParameters():
    #gets the ip address, user nickname and port number from the command line.
    try:
        ip = sys.argv[1]
        user = sys.argv[2]
        port = sys.argv[3]
    except:
        #catches if any argument is blank
        print("Format: IP address username port number eg 127.0.0.1 user 8080")
        sys.exit()
    try:
        # ensures the port is valid
        port = int(port)
    except:
        print("Port number (third input) must be an integer")
        sys.exit()
    return ip, user, port

def receiveMessage():
    #receive a message
    os.system("")
    newLine = '\033[D'
    while 1:
        try:
            message = clientSocket.recv(1024).decode()
            if message == 'USERNAME':
                # the client sends the username to the server before any input
                clientSocket.sendall(user.encode())
            elif message == 'USERNAME TAKEN':
                # the username must be unique
                print('The username you have chosen is already in use. Please try again')
                clientSocket.close()
                break
            else:
                #prints the message from the server
                #ensures the user always has a prompt to write their message
                print(f'{newLine}'+message+'\n>', end='')
        except:
            print(f"{newLine}"+"An error occured!")
            clientSocket.close()
            break
    os._exit(0)

def writeMessage():
    #send a message
    while 1:
        message = input('')
        if message == 'exit':
            #user leaves the server
            os._exit(0)
        else:
            message = f'{user}: {message}'
            clientSocket.sendall(message.encode())

ip, user, port = getParameters()
try:
    #try and connect to the server
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
    clientSocket.connect((ip, port))
    # start threads
    receive_thread = threading.Thread(target=receiveMessage)               #receiving multiple messages
    receive_thread.start()
    write_thread = threading.Thread(target=writeMessage)                   #sending messages 
    write_thread.start()
except:
    #if something is wrong.
    print('Server is unavailable or the IP address / port number is incorrect. \nCheck IP address and host and try again later')
    sys.exit()