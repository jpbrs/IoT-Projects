from Crypto.Cipher import AES
import binascii
import os
    

key = "abcdefghijklmnop"

encryptor = AES.new(key, AES.MODE_ECB)

text = "Tech tutorials x"

ciphertext = encryptor.encrypt(text)
joe = encryptor.decrypt(ciphertext)

print(joe)

print(ciphertext)
print(binascii.hexlify(ciphertext))
print(binascii.unhexlify())
