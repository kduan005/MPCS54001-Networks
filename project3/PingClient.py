import sys
import os
import time
import socket
import pingmsg
import threading

class PingClient(object):
    """docstring forPingmsg."""

    def __init__(self, server_ip, server_port, count, period, timeout):
        self.server_ip = server_ip
        self.server_port = server_port
        self.count = count
        self.period = period
        self.timeout = timeout
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.clientSocket.connect((server_ip, server_port))

    def run(self):

        def _ping(seqno):
            pmsg = pingmsg.Pingmsg(8, 0, os.getpid(), seqno, current_milli_time())
            pmsg.setChecksum()
            self.clientSocket.sendto(pmsg.toByte(), (self.server_ip, self.server_port))
            reply = pingmsg.Pingmsg.fromBytes(self.clientSocket.recv(2048))
            print(current_milli_time() - reply.getTimestamp())
            print(reply.verifyChecksum())

        for seqno in range(self.count):
            t = threading.Timer(self.period/1000 * seqno, _ping, [seqno])
            t.start()

# https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
current_milli_time = lambda: int(round(time.time() * 1000))

if __name__ == "__main__":
    errmsg = "Usage: python3.7 PingClient.py --server_ip=<server ip addr>\n\
                \t--server_port=<server port>\n\
                \t--count=<number of pings to send>\n\
                \t--period=<wait interval>\n\
                \t--timeout=<timeout>"
    # exit when there are not enough command-line arg supplied, show usage message
    if len(sys.argv) < 6:
        sys.exit(errmsg)

    # read in arguments from input
    server_ip = server_port = count = period = timeout = ""
    for arg in sys.argv[1:]:
        k, v = arg.split("=")
        if k == "--server_ip":
            server_ip = v
        elif k == "--server_port":
            server_port = int(v)
        elif k == "--count":
            count = int(v)
        elif k == "--period":
            period = int(v)
        elif k == "--timeout":
            timeout = v
    # exit when input malformatted, show usage message
    if not (server_ip and server_port and count and period and timeout):
        sys.exit(errmsg)
    # instantiate Pingmsg object
    else:
        pc = PingClient(server_ip, server_port, count, period, timeout)
        pc.run()
