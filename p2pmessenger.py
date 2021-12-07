import socket
import threading
import sys
from getopt import getopt

def receiver(address):
    with socket.socket() as s:
        s.bind(address)  # assigns the IP address and the port number to this socket instance
        s.listen(1)  # 1 specifies the number of unaccepted connections that the system will allow before refusing new connections
        while True:
            connection, (peer_ip, _) = s.accept()  # Wait for a new connection to come in and Establish a socket for communications if so. accept() returns a socket of the other side on this connection. 
            with connection:     
                message = connection.recv(1024).decode() # Maximally receive 1024 bytes and convert them into message. 
                print("{}: {}".format(peer_ip, message))

def sender(address):
    while True:
        message = input(">> ")  
        with socket.socket() as s:
            s.connect(address)    # The method enables the sender's socket to connect to the destination socket; address is a Tuple which includes both IP address and port number of the destination
            s.sendall(message.encode())  # sendall: send the entire buffer you have or throw an exception. message.encod: covert the message to binary streams.

def start():
    o = dict(getopt(sys.argv[1:], 'h:p:l:')[0])  # covert a list of Tuples input from the command line to a dictionary for the service. h: destination IP address or hostname; p: destination port number; l: receiving port number at source
    threading.Thread(target=receiver, args=(('', int(o.get('-l',8080))),)).start()  # -l is the port number that I am receiving. target=receiver: call receiver method on a new thread. '' inside args should be the IP address of this receiver which is blank because reciever doesn't need to get its own IP address. (o.get('-l',8080): use the port number input by "-l" to listening. If no "-l" in the command line, use the default 8080.
    threading.Thread(target=sender, args=((o.get('-h',''),int(o.get('-p',8080))),)).start() # -p is the port number that the receiver is receiving. target=sender: call sender method on a new thread. get('-h',''): sender gets the receiver's IP address from the command line. o.get('-p',8080): sender gets the 

if __name__ == "__main__":
    start()