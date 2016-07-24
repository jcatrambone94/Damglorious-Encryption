import aes_dec
import aes_enc
import sys


Usage = "Usage: python Damglorious-Encryption.py <e/d> <Password> <Input Path> <Output Path>"



if len(sys.argv) < 4:
	print Usage
	sys.exit(0)

else:
	EncOrDec = sys.argv[1]
	password = sys.argv[2]
	inputPath = sys.argv[3]
	outputPath = sys.argv[4]

	if EncOrDec == "e":
		encrypter = aes_enc.AES_Enc(verbose=False)
		encrypter.encrypt(password,inputPath,outputPath)

	elif EncOrDec == 'd':
		decrypter = aes_dec.AES_Dec(verbose=False)
		decrypter.decrypt(password,inputPath,outputPath)

	else:
		print Usage
