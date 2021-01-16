#! /usr/bin/python
#Linux   : pip3 install -i https://pypi.douban.com/simple pycryptodome 
#windows : pip3 install -i https://pypi.douban.com/simple pycryptodomex
#Optinal : pip install cryptography  
import rsa
import json
from binascii import b2a_hex, a2b_hex

class rsacrypt():
    def __init__(self, pubkey, prikey):
        self.pubkey = pubkey
        self.prikey = prikey

    def encrypt(self, text):
        self.ciphertext = rsa.encrypt(text.encode(), self.pubkey)
        # 因为rsa加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        decrypt_text = rsa.decrypt(a2b_hex(text), prikey)
        return decrypt_text


if __name__ == '__main__':
    pubkey, prikey = rsa.newkeys(256)
    # fail below 
    # with open("pubkey.json", "w") as fp:
    #     json.dump(pubkey, fp, indent=4)
    # with open("prikey.json", "w") as fp:
    #     json.dump(prikey, fp, indent=4)
    rs_obj = rsacrypt(pubkey,prikey)
    text='hello'
    ency_text = rs_obj.encrypt(text)
    print(ency_text)
    print(rs_obj.decrypt(ency_text))
