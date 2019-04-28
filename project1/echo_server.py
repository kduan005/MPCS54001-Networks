import sys
from socket import *

def echo(port):
    serverPort = port
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    while True:
        connectionSocket, addr = serverSocket.accept()
        echoRequest = connectionSocket.recv(2048).decode()
        echoReply = echoRequest
        sys.stdout.write(echoReply)
        connectionSocket.send(echoReply.encode())
        connectionSocket.close()

if __name__ == "__main__":
    echo(int(sys.argv[1]))
