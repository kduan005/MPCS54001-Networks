import asyncore, socket

class HTTPClient(asyncore.dispatcher):

    def __init__(self, host, id):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, 7777) )
        self.buffer = "Hi there %d" % id

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print self.recv(8192)

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


client1 = HTTPClient('localhost', 1)
client2 = HTTPClient('localhost', 2)
asyncore.loop()
