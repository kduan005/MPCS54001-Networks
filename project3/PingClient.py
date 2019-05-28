import sys
import os
import socket
import pingmsg
import threading
from statistics import mean
from ctime import current_milli_time

class PingClient(object):
    """
    PingClient class is a simulation of ICMP echo request client that sends
    echo requests periodically to PingServer
    It has the following attributes:
        server_ip: the IP address of the PingSever it wants to send requests to
        server_port: the port the PingServer is listening to
        count: the number of ping requests the PingClient will send
        period: the intermission between two sendings
        timeout: the time after which the data exchange will expire if the client
            failed to receive the reply
    """
    def __init__(self, server_ip, server_port, count, period, timeout):
        self.server_ip = server_ip
        self.server_port = server_port
        self.count = count
        self.period = period
        self.timeoutCount = 0
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientSocket.settimeout(timeout/1000)

    def run(self):
        '''
        the run() function drives the client's sending of requests
        '''

        def _ping(seqno):
            '''
            a single sending of request by the client, will be called periodically
            '''
            # generate a ping message and set the values for ICMP headers
            # header values are:
            # type = 8, code = 0, identifier = process id, seqno = sequence number
            # the ping message being sent to the server, timestamp = current time
            pmsg = pingmsg.Pingmsg(8, 0, os.getpid(), seqno, current_milli_time())
            # set checksum for the ping message
            pmsg.setChecksum()
            # send ping message to server
            self.clientSocket.sendto(pmsg.toByte(), \
            (self.server_ip, self.server_port))
            # receive echo message from server
            try:
                # convert message to a Pingmsg object
                reply = pingmsg.Pingmsg.fromBytes(self.clientSocket.recv(2048))
                # compute round trip time
                duration = current_milli_time() - reply.getTimestamp()
                # verify if checksum is valid
                if reply.verifyChecksum():
                    # if checksum is valid, print message info, record rtt for
                    # aggregate statistics
                    print("PONG {}: seq={} time={} ms".format(self.server_ip, \
                    seqno, duration))
                    durations.append(duration)
                else:
                    # if checksum not valid, treat it as if timeout
                    self.timeoutCount += 1
                    print("Checksum verification failed for echo reply seqno={}"\
                    .format(seqno))
            except socket.timeout:
                # when reply times out, increment timeout count
                self.timeoutCount += 1

        # durations list for aggregating rtt
        durations = []

        print("PING " + self.server_ip)

        # start time of entire run process
        start = current_milli_time()
        # spawn a thread for each ping message, use threading.Timer to schedule
        # sending periodically
        threads = []
        for seqno in range(1, self.count+1):
            threads.append(threading.Timer(self.period/1000 * (seqno-1),\
             _ping, [seqno]))
            threads[-1].start()

        # let the main thread to wait for all spawned threads to finish
        [thread.join() for thread in threads]

        # end time of the receiving of the last reply or timeout
        end = current_milli_time()

        # print aggregate statistics
        print("\n--- {} ping statistics ---".format(self.server_ip))
        print("{} transmitted, {} received, {:.0%} loss, time {} ms".format(\
        self.count, self.count - self.timeoutCount, self.timeoutCount/self.count,\
        end - start))
        try:
            # when durations list is not empty
            min_duration = min(durations)
            mean_duration = round(mean(durations))
            max_duration = max(durations)
        except:
            # when all threads time out and there's no rtt data in durations list
            min_duration = mean_duration = max_duration = 0
        print("rtt min/avg/max = {}/{}/{}".format(min_duration, \
        mean_duration, max_duration))



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
            timeout = int(v)
    # exit when input malformatted, show usage message
    if not (server_ip and server_port and count and period != "" and timeout):
        sys.exit(errmsg)
    # instantiate PingClient object and run ping requests
    else:
        pc = PingClient(server_ip, server_port, count, period, timeout)
        pc.run()
