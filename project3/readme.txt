Overview:
    The project implements a UDP-based ping client using asynchronous socket.
    It spawns a new thread when there needs to send a new echo request from the
    client. The client emulates some of the standard ping utility functionality
    available in modern operating systems, except that it uses UDP rather than
    raw IP sockets. The ICMP protocol is used when transmitting data in the
    data payload from a UDP datagram.

Language:
    The project is written in python3.7 and can be executed for python3.7

Executables and libraries:
    PingClient.py: the driver file that runs the client and sends the echo requests
    pingmsg.py: pingmsg library contains definition of Pingmsg class which represents
        a ping/pong message
    ctime.py: ctime library contains the auxiliary function to get current time
        in millisecond's format since the UNIX epoch

Usage:
    1. Put both Ping server and Ping client in a same directory, including:
        PingClient.py
        pingmsg.py
        ctime.py
        pingmsg.jar (provided by professor to test the implementation of the client)
        PingServer.java (provided by professor to test the implementation of the client)

    2. Compile the server:
        $ javac -cp .:pingmsg.jar PingSever.java

    3. Run the ping server:
        $ java -cp .:pingmsg.jar PingServer --port=<port>
                                           [--lost_rate=<rate>]
                                           [--bit_error_rate=<rate>]
                                           [--avg_delay=<delay>]
        Arguments instructions:
        lost_rate: simulated packet lost rate, ranging from 0.0 to 1.0
        bit_error_rate: simulated bit_error occurrence rate, ranging from 0.0 to 1.0
        avg_delay: simulated transmission delay in milliseconds when client and sever
        on the same machine or are close on the network, default is 100

    3. Run ping client:
        $ python3.7 PingClient.py --server_ip=<server ip addr>
                                  --server_port=<server port>
                                  --count=<number of pings to send>
                                  --period=<wait interval>
                                  --timeout=<timeout>
        Arguments instructions:
        count: how many ping echo requests to send
        period: the interval between the sending of two echo requests, meaningly
        ping requests are sent periodically
        timeout: after how much time long a request session should timeout when packet
        loss occurs

        Examples:
            $ python3.7 PingSever.py --server_ip=127.0.0.1
                                     --server_port=56789
                                     --count=10
                                     --period=1000
                                     --timeout=60000
        Output:
            PING 127.0.0.1
            PONG 127.0.0.1: seq=2 time=1233 ms
            PONG 127.0.0.1: seq=1 time=658 ms
            PONG 127.0.0.1: seq=5 time=2966 ms
            PONG 127.0.0.1: seq=4 time=1420 ms
            PONG 127.0.0.1: seq=6 time=898 ms
            PONG 127.0.0.1: seq=3 time=45 ms
            PONG 127.0.0.1: seq=7 time=3630 ms
            PONG 127.0.0.1: seq=8 time=1279 ms
            PONG 127.0.0.1: seq=10 time=2420 ms
            PONG 127.0.0.1: seq=9 time=3253 ms

            --- 127.0.0.1 ping statistics ---
            10 transmitted, 10 received, 0% loss, time 12258 ms
            rtt min/avg/max = 45/1780/3630

Results:
    The program can handle all sample tests provided including:
    Basic operation:
    $ python3.7 PingSever.py --server_ip=127.0.0.1
                             --server_port=56789
                             --count=10
                             --period=1000
                             --timeout=60000
    Different count:
    $ python3.7 PingSever.py --server_ip=127.0.0.1
                             --server_port=56789
                             --count=5
                             --period=1000
                             --timeout=60000
    Different period:
    $ python3.7 PingSever.py --server_ip=127.0.0.1
                             --server_port=56789
                             --count=10
                             --period=2000
                             --timeout=60000
    Large average delay:
    $ java -cp .:pingmsg.jar PingServer --port=56789
                                        --lost_rate=0.0
                                        --bit_error_rate=0.0
                                        --avg_delay=5000
    $ python3.7 PingSever.py --server_ip=127.0.0.1
                             --server_port=56789
                             --count=10
                             --period=1000
                             --timeout=60000
    High packet loss rate:
    $ java -cp .:pingmsg.jar PingServer --port=56789
                                        --lost_rate=0.75
                                        --bit_error_rate=0.0
                                        --avg_delay=100
    $ python3.7 PingSever.py --server_ip=127.0.0.1
                             --server_port=56789
                             --count=10
                             --period=1000
                             --timeout=10000
    High bit error rate
    $ java -cp .:pingmsg.jar PingServer --port=56789
                                        --lost_rate=0.0
                                        --bit_error_rate=0.75
                                        --avg_delay=100
    $ python3.7 PingSever.py --server_ip=127.0.0.1
                             --server_port=56789
                             --count=10
                             --period=1000
                             --timeout=10000
    Short timeout:
    $ java -cp .:pingmsg.jar PingServer --port=56789
                                        --lost_rate=0.0
                                        --bit_error_rate=0.0
                                        --avg_delay=10000
    $ python3.7 PingSever.py --server_ip=127.0.0.1
                             --server_port=56789
                             --count=10
                             --period=1000
                             --timeout=2000
    Long timeout:
    $ java -cp .:pingmsg.jar PingServer --port=56789
                                        --lost_rate=0.0
                                        --bit_error_rate=0.0
                                        --avg_delay=2000
    $ python3.7 PingSever.py --server_ip=127.0.0.1
                             --server_port=56789
                             --count=10
                             --period=1000
                             --timeout=20000
    Timeout(No server):
    $ python3.7 PingSever.py --server_ip=127.0.0.1
                             --server_port=56789
                             --count=10
                             --period=1000
                             --timeout=100
