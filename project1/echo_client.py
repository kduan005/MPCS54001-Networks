import sys
from socket import *

def echo(host, port):
    serverName = host
    serverPort = port
    while True:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        echoRequest = sys.stdin.readline()
        clientSocket.send(echoRequest.encode())
        echoReply = clientSocket.recv(2048)
        sys.stdout.write(echoReply)
        clientSocket.close()

if __name__ == "__main__":
    echo(sys.argv[1], int(sys.argv[2]))
