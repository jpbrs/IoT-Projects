import hashlib

secret = "Esse eh o segredo"
bsecret = secret.encode() # Passa p bytes
print(bsecret)

funcao=hashlib.md5()
funcao.update(bsecret)

print(funcao.digest())

compare_secret = "Esse eh o segredo"
bcompare = compare_secret.encode()
print(bcompare)

funcao_compare = hashlib.md5()
funcao_compare.update(bcompare)

if funcao.digest() == funcao_compare.digest():
    print("True")

from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(" key :",key)

f = Fernet(key)
message = b"Secrets go here"
encrypted = f.encrypt(message)
print(encrypted)
print(f.decrypt(encrypted))

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

private_key = rsa.generate_private_key(public_exponent=65537,key_size = 4096, backend = default_backend())


public_key = private_key.public_key
print("Public Key : {}".format(public_key))
public_key = private_key.public_key()
print("Public Key : {}".format(public_key))


from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

encrypted = public_key.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
print(encrypted)
decrypted = private_key.decrypt(encrypted, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
print(decrypted)