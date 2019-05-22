class Pingmsg(object):
    """docstring for Pingmsg."""

    def __init__(self, type, code, identifier, seqno, timestamp):
        self.type = type
        self.code = code
        self.checksum = 0
        self.identifier = identifier
        self.seqno = seqno
        self.timestamp = timestamp
        self.msg = b""

    def _onesComplementSum(self):
        # https://stackoverflow.com/questions/1767910/checksum-udp-calculation-python
        # helper function to calculate one's complement sum of two numbers
        def _carry_around_add(a, b):
            c = a + b
            return (c & 0xffff) + (c >> 16) #first 16 bits plus carry-around

        byte_wo_checksum = self.toByte()
        s = 0
        # taking every 16 bits of the header and compute the one's complement sum
        for i in range(0, 14, 2):
            num = int.from_bytes(byte_wo_checksum[i:(i+2)], byteorder="big")
            s = _carry_around_add(s, num)

        return s

    def setChecksum(self):
        s = self._onesComplementSum()
        # first 16bits of one's complement of one's complement sum
        self.checksum = ~s & 0xffff

    def verifyChecksum(self):
        s = self._onesComplementSum()
        #check if all bits are ones
        return s == 65535

    def toByte(self):
        #convert all header fields to byte arrays
        return (self.type).to_bytes(1, byteorder="big")\
             + (self.code).to_bytes(1, byteorder="big")\
             + (self.checksum).to_bytes(2, byteorder="big")\
             + (self.identifier).to_bytes(2, byteorder="big")\
             + (self.seqno).to_bytes(2, byteorder="big")\
             + (self.timestamp).to_bytes(6, byteorder="big")

    @staticmethod
    def fromBytes(msg):
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
