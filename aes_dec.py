import sys, datetime, struct, zlib_wrapper, zlib
import random, string, hmac, os, pwd, hashlib, base64
from Crypto.Cipher import AES
import pdb

class AES_Dec():
    def __init__(self, verbose=False):
        self.verbose = verbose
        done = False

    def checkVerison(self,versionMajor, versionMinor):
        if versionMajor == 1 and versionMinor == 1:
            if self.verbose:
                print "passed version check"
            return True
        else:
            if self.verbose:
                print "failed version check"
                print "Version: " + str(versionMajor) + ":" + str(versionMinor)
            return False

    def checkCRC(self,headerCrc, packetCrc):
        if headerCrc == packetCrc:
            return True
        else:
            return False

    def check_chunkSize(self, data):
        """
        :param packet: Encrypted packet with Header attached
        :param key: Must be the same key used in encryption
        :return: headlessData, passCorrect
        """
        Header = struct.unpack("!BBII16sI32s", data[:62])
        sizeOfChunk = Header[3]
        return sizeOfChunk

    def check_iv(self, data):
        """
        :param packet: Encrypted packet with Header attached
        :param key: Must be the same key used in encryption
        :return: headlessData, passCorrect
        """
        Header = struct.unpack("!BBII16sI32s", data[:62])
        VM = Header[0]
        Vm = Header[1]
        iv = Header[4]
        headlessData = data[62:]
        if self.checkVerison(VM,Vm):
            return iv

    def strip_header(self, data):
        """
        :param packet: Encrypted packet with Header attached
        :param key: Must be the same key used in encryption
        :return: headlessData, passCorrect
        """
        #if self.verbose:
            #print "header: %d" %len(data)
        if len(data) < 62:
            print len(data)
            return False
        else:
            Header = struct.unpack("!BBII16sI32s", data[:62])
            headlessData = data[62:]
            return headlessData

    def getNextChunkSize(self, data):

        if len(data) != 0:
            Header = struct.unpack("!BBII16sI32s", data[:62])
            sizeOfChunk = Header[3]
            return sizeOfChunk

    def getPadSize(self, data):

        if len(data) != 0:
            Header = struct.unpack("!BBII16sI32s", data[:62])
            padSize = Header[5]
            return padSize
    def getHMAC(self, data):

        if len(data) != 0:
            Header = struct.unpack("!BBII16sI32s", data[:62])
            HMAC = Header[6]
            return HMAC

    def checkHMAC(self,HMAC, data,key):
        hmacDigest = hmac.new(key,data,hashlib.sha256).digest() 
        if hmac.compare_digest(hmacDigest,HMAC):
            if self.verbose:
                print "HMAC Verification Passed"
            return True
        else:
            if self.verbose:
                print "HMAC Verification Failed"
                print "Wrong Password"
                print "try again"
            return False

    def decrypt(self, password, in_filename, out_filename, chunksize=64*1024):
        """
        :param key: Must be same key from encryption
        :param in_filename: File name of the file to be decrypted
        :param out_filename: If no name given it will be the same as the original
        :param chunksize: This is the size of the chunk to be decrypted
        :return: None
        """
        #pdb.set_trace()
        infile = open(in_filename, 'rb' )
        chunk = infile.read(chunksize)
        if self.checkVerison:
            iv = self.check_iv(chunk)
            sizeOfChunk = self.check_chunkSize(chunk)
            key = hashlib.sha256(password).digest()
            decryptor = AES.new(key, AES.MODE_CBC, iv)
            infile.close()
            counter = 0
            infile = open(in_filename, 'rb' )
            outfile = open(out_filename, 'wb')
            compresser = zlib_wrapper.compress()
            fileSize = os.path.getsize(in_filename)
            packetCounter = 0
            while True:
                if counter == fileSize:
                    break
                chunk = infile.read(int(sizeOfChunk + 62))

                HMAC = self.getHMAC(chunk)
                headlessData = self.strip_header(chunk)
                if self.checkHMAC(HMAC,headlessData,key):
                    counter += int(sizeOfChunk + 62)
                    trueSize = self.getPadSize(chunk)
                    if self.verbose:
                        print "len Headless: %d" % len(headlessData)
                        print "Packet #: %d" % packetCounter
                    dec_data = decryptor.decrypt(headlessData)
                    decomp_data = compresser.dec_data(dec_data)
                    nextHeader = infile.readlines(int(sizeOfChunk + 62))
                    header = ''
                    for line in nextHeader:
                        header += line
                    sizeOfChunk = self.getNextChunkSize(header)
                    if self.verbose:
                        print "counter: %d" % counter
                    infile.seek(counter,0)
                    Data = decomp_data['data']
                    if self.verbose:
                        print "final chunk size: %d" % len(Data)
                    outfile.write(Data)
                    packetCounter += 1
                    if self.verbose:
                        print "I wrote a good packet"
                else:
                    sys.exit(0)
            print "Packets Decrypted: %d" % packetCounter
            if self.verbose:
                print "Counter: %s = FileSize: %s" % (counter, fileSize)
        infile.close()
        outfile.close()
            
        




    
       



    
       
