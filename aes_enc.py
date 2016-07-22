import sys, datetime, struct, zlib_wrapper, time
import random, string, hmac, os, pwd, hashlib, base64
from Crypto.Cipher import AES
from Crypto import Random
import pdb

class AES_Enc():
    def __init__(self, verbose=False):
        self.verbose = verbose
        done =False

    def build_header(self, data, prePadSize,postPadSize,hmacDigest,versionMajor, versionMinor, iv):
        """
        :param data: data to build header onto
        :param versionMajor: Release number
        :param versionMinor: Patch number
        :return: built_data
        """
        padSize = postPadSize - prePadSize
        if self.verbose:
            print "Pading Size = %d" % padSize 
        sizeOfChunk = len(data)
        t0, t1, t2, t3, t4, t5, t6, t7, t8 = time.gmtime()
        tStamp = time.mktime((t0, t1, t2, t3, t4, t5, 0, 0, 0))
        header = struct.pack("!BBII16sI32s",versionMajor,versionMinor,tStamp,sizeOfChunk, iv,padSize,hmacDigest)
        built_data = header + data
        return built_data

    def encrypt(self, password, data, outputName, outputPath=os.getcwd(),chunksize=64*1024):
        
        """
        :param key: String that will operate as the password
        :param in_filename: Name of input file
        :param outputName: Name of the encrypted file
        :param outputPath: Path of the encrypted data
        :param chunksize: Sets the size of the chunk that the function uses to encrypt the file.
        :return: None
        """
        iv = Random.new().read(16)

        key = hashlib.sha256(password).digest()
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        compresser = zlib_wrapper.compress()
        os.chdir(outputPath)
        infile = open(data, 'rb')
        outfile = open(outputName, 'wb')
        packetCounter = 0
        while True:                                                                 # Loop to split the data into 64k Chunks
            chunk = infile.read(chunksize)
            if len(chunk) == 0:                                                     #Breaks loop if EOF
                break

            crc = compresser.crc32_data(chunk)
            if self.verbose:
                print  "chunk size: %d" % len(chunk)
            comp_chunk = compresser.comp_data(chunk)
            if self.verbose:
                print "comp size: %d" %len(comp_chunk)
            fin_comp_chunk = compresser.build_header(comp_chunk,crc)
            prePadSize = len(fin_comp_chunk)
            if self.verbose:
                print "pre padding size: %d" % prePadSize
                print "Packet #: %d" % packetCounter
            if len(fin_comp_chunk) == 0:                                                # Breaks loop if there is no more data left
                break
            elif len(fin_comp_chunk) % 16 != 0:                          
                fin_comp_chunk += '#' * (16 - len(fin_comp_chunk) % 16)                     # Padding logic
            postPadSize = len(fin_comp_chunk)
            if self.verbose:
                print "post pad size: %d" % postPadSize
            preEncCrC = compresser.crc32_data(fin_comp_chunk)
            encrypted_data = encryptor.encrypt(fin_comp_chunk)
            HMACDigest = hmac.new(key,encrypted_data,hashlib.sha256).digest()                        # Encrypt Data
            encrypted_Packet = self.build_header(encrypted_data, prePadSize,postPadSize,HMACDigest,1, 1,iv)
            if self.verbose:
                print "encrypted_Packet size: %d" % len(encrypted_Packet)
            packetCounter += 1
            if self.verbose:
                print "I encrypted a packet"
            outfile.write(encrypted_Packet)
        print "Encrypted Packets: %d" %packetCounter
        outfile.close()
        infile.close()


