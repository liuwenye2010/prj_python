#!/usr/bin/env python3
# pycypto had been out of date
#Linux   : pip3 install -i https://pypi.douban.com/simple pycryptodome 
#windows : pip3 install -i https://pypi.douban.com/simple pycryptodomex
import sys
import  base64
#from Crypto.Cipher import AES  
from Cryptodome.Cipher import AES
from binascii import b2a_hex, a2b_hex

'''
AES usage
'''
# value should be 16 bytes padped (16*8=128bits)
def padded_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # bytes

def encrypt(key, text):
    aes = AES.new(padded_to_16(key), AES.MODE_ECB)  
    encrypt_aes = aes.encrypt(padded_to_16(text))  # AES enc
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # encode bytes as base64
    return encrypted_text

def decrypt(key, text):
    aes = AES.new(padded_to_16(key), AES.MODE_ECB)  
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))  # decode as bytes from base64
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')  # dec to return orig values
    return decrypted_text

if __name__ == "__main__":
    print(sys.version)
    key = "123456"
    text = "hello aes"
    encrypt_result = encrypt (key,text)
    print('ENC:' + encrypt_result)
    decrypt_text   = decrypt (key,encrypt_result)
    print('DEC:' + decrypt_text)
    pass