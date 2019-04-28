import os
import collections
import glob

class Generator(object):
    '''
    Generator class to generate response from tokens
    '''
    def __init__(self, tokens):
        self.tokens = collections.defaultdict(lambda: None)
        self.tokens.update(tokens)

    def gen_response(self):
        #when method from request is neither "GET" or "HEAD"
        if self.tokens["method"] not in {b"GET", b"HEAD"}:
            return self.gen_405()

        request_file = self.tokens["object"]
        _, file_extension = os.path.splitext(self.tokens["object"])

        #request_file is www/redirect.defs
        if file_extension == b".defs":
            return self.gen_404()
        #request_file type is not supported
        elif file_extension not in {b".html", b".plain", b".pdf", b".png", b".jpeg"}:
            return self.gen_405()
        #elif tokens["object"] found in redirect.defs:
        #   return self.gen_301()
        else:
            cand_files = glob.iglob(request_file, recursive=True)
            try:
                #successfully find file in the current directory
                request_file_path = next(cand_files)
                return self.gen_200(request_file_path)
            except StopIteration:
                #cannot find file in the current directory
                return self.gen_404()


    def gen_GET(self):

        return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 9\r\n\r\nHello Ke!"

    def gen_HEAD(self):
        return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 9\r\n\r\nHello Ke!"

    def gen_404(self):
        self.tokens["status"] = "404"
        self.tokens["phrase"] = "Not Found"
        return b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 7\r\n\r\n404 Ke!"

    def gen_301(self):
        self.tokens["status"] = "301"
        self.tokens["phrase"] = "Moved Permanently"
        pass

    def gen_200(self, request_file_path):
        self.tokens["status"] = "200"
        self.tokens["phrase"] = "OK"
        if self.tokens["method"] == "GET":
            return self.gen_GET()
        elif self.tokens["method"] == "HEAD":
            return self.gen_HEAD()

    def gen_400(self):
        #when receiving malformed request
        self.tokens["status"] = "400"
        self.tokens["phrase"] = "Bad Request"
        return b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\nContent-Length: 7\r\n\r\n400 Ke!"

    def gen_405(self):
        #when request method not allowed
        self.tokens["status"] = "405"
        self.tokens["phrase"] = "Method Not Allowed"
        return b"HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\nContent-Length: 7\r\n\r\n405 Ke!"

#len(s.encode('utf-8'))
