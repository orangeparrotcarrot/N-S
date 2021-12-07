import socket
import select

ip = '192.168.139.1'
port = 8800
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#overcomes address already in use error, allows us to reuse an address
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((ip,port))
serversocket.listen()

socketslist = [serversocket]
clients = {}
print(f"listening for connections on {ip}:{port}")

def receivemessage(clientsocket):
    try:
        messageheader = clientsocket.recv(10)
        if not len(messageheader):
            return False
        messagelength = int(messageheader.decode().strip())
        return clientsocket.recv(messagelength)
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(socketslist, [], socketslist)
    # Iterate over notified sockets
    for notified_socket in read_sockets:

        # If notified socket is a server socket - new connection, accept it
        if notified_socket == serversocket:

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = serversocket.accept()

            # Client should send his name right away, receive it
            user = receivemessage(client_socket)
            print(user)

            # If False - client disconnected before he sent his name
            if user is False:
                continue

            # Add accepted socket to select.select() list
            socketslist.append(client_socket)

            # Also save username and username header
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user.decode('utf-8')))

        # Else existing socket is sending a message
        else:

            # Receive message
            message = receivemessage(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket()
                socketslist.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]

            print(f'>{user.decode("utf-8")}: {message.decode("utf-8")}')

            # Iterate over connected clients and broadcast message
            for client_socket in clients:

                # But don't sent it to sender
                if client_socket != notified_socket:

                    # Send user and message (both with their headers)
                    # We are reusing here message header sent by sender, and saved username header send by user when he connected
                    client_socket.send(user + message)

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        socketslist.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]