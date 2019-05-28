class Pingmsg(object):
    """
    Pingmsg class has the essential attributes of a ping message including
    type: message type, 8 for echo request and 0 for echo reply
    code: always 0
    checksum: internet checksum computed over message
    identifier: arbitrary unsigned integer (always consistent for entire duration
        of process, and is set to be the process ID for this program)
    seqno: sequence number starting at 1 and incremented for each successive ping
        message sent by the client
    timestamp: unsigned integer representing the number of milliseconds since
        the UNIX epoch
    """

    def __init__(self, type, code, identifier, seqno, timestamp):
        self.type = type
        self.code = code
        self.checksum = 0
        self.identifier = identifier
        self.seqno = seqno
        self.timestamp = timestamp

    def _onesComplementSum(self):
        '''
        function to calculate one's complement sum of all 16 bits-formed hearder
        chunks
        '''

        def _carry_around_add(a, b):
            '''
            helper function to calculate one's complement sum of two numbers
            https://stackoverflow.com/questions/1767910/checksum-udp-calculation-python
            '''
            c = a + b
            # take the last 16 bits and wrap around carry before the MSB if any
            return (c & 0xffff) + (c >> 16)

        # convert Pingmsg object to byte, checksum is initially set to 16-bit 0
        byte_wo_checksum = self.toByte()
        # one's complement sum
        s = 0
        # taking every 16 bits of the header and compute the one's complement sum
        # of the current sum and the new chunk
        for i in range(0, 14, 2):
            # 14 bytes in total in the hearder, read every two of them once
            num = int.from_bytes(byte_wo_checksum[i:(i+2)], byteorder="big")
            s = _carry_around_add(s, num)

        return s

    def setChecksum(self):
        '''
        set checksum to Pingmsg object
        '''
        s = self._onesComplementSum()
        # take the first 16 bits of one's complement of the one's complement sum
        self.checksum = ~s & 0xffff

    def verifyChecksum(self):
        '''
        verify if the checksum of a Pingmsg object is valid
        '''
        s = self._onesComplementSum()
        #check if all bits are ones, i.e. 2 ^ 16 - 1
        return s == 65535

    def toByte(self):
        '''
        convert all header fields to byte arrays
        '''
        return (self.type).to_bytes(1, byteorder="big")\
             + (self.code).to_bytes(1, byteorder="big")\
             + (self.checksum).to_bytes(2, byteorder="big")\
             + (self.identifier).to_bytes(2, byteorder="big")\
             + (self.seqno).to_bytes(2, byteorder="big")\
             + (self.timestamp).to_bytes(6, byteorder="big")

    @staticmethod
    def fromBytes(msg):
        '''
        convert a byte array of message to a Pingmsg object
        '''
        type = msg[0]
        code = msg[1]
        checksum = int.from_bytes(msg[2:4], byteorder="big")
        identifier = int.from_bytes(msg[4:6], byteorder="big")
        seqno = int.from_bytes(msg[6:8], byteorder="big")
        timestamp = int.from_bytes(msg[8:], byteorder="big")
        p = Pingmsg(type, code, identifier, seqno, timestamp)
        p.checksum = checksum
        return p

    def getTimestamp(self):
        return self.timestamp
