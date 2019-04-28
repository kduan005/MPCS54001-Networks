import os

class Parser(object):
    '''
    Parser class to parse the request and return tokens
    '''
    def parse_request(self, request):
        headers = request.split(b"\r\n")

        #GET /favicon.ico HTTP/1.1
        method, obj, version = headers[0].split(b" ")
        #Host: localhost:8080
        host_port = headers[1].split(b": ")[1].split(b":")
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else "" #port maynot present
        #Connection: keep-alive
        persist = True if headers[2].split(b": ")[1] == "keep-alive" else False

        tokens = {"method": method,
                  "object": self.path(obj),
                  "version": version,
                  "persist": persist}

        return tokens

    def path(self, obj):

        return (os.path.dirname(os.path.abspath(__file__)) + "/www/**" + obj.decode("utf-8")).encode()
