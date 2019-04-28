import asyncore
import socket
import sys
import parser
import generator

# handler and dispatcher refer to https://docs.python.org/2/library/asyncore.html
class MyHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        request = self.recv(8192)
        if request:
            p = parser.Parser()
            tokens = p.parse_request(request)
            print (tokens)
            r = generator.Generator(tokens)
            response = r.gen_response()
            self.send(response)


class MyServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print ('Incoming connection from %s' % repr(addr))
            handler = MyHandler(sock)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python web_server.py -port")
    port = int(sys.argv[1])
    server = MyServer('localhost', port)
    asyncore.loop()
