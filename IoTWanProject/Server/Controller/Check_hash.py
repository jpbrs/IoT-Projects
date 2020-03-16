from Crypto.Cipher import AES
import binascii
import os

def check_MIC(MIC : str,dUI : str,aUI : str,number : str, key : str):
    encryptor = AES.new(key, AES.MODE_ECB)
    text = dUI+aUI+number

    ciphertext = encryptor.encrypt(text)
    a = binascii.hexlify(ciphertext)
    a = a.decode()

    return(MIC == a)

# key = "abcdefghijklmnop"
# text = "Tech tutorials x"

ciphertext = encryptor.encrypt(text)

a = binascii.hexlify(ciphertext)
a = a.decode()

print(a)