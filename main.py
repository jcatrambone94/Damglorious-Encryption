import aes_dec
import aes_enc

encrypter = aes_enc.AES_Enc(verbose=False)
decrypter = aes_dec.AES_Dec(verbose=False)

encrypter.encrypt("password", 'rockyou.txt', 'test')
decrypter.decrypt("password", 'test','test.txt')
