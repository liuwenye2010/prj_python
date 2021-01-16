#! /usr/bin/python
import random  
import hashlib

def md5_demo (): 
    print("PY:MD5")
    m = hashlib.md5()
    data = "hello MD5"
    m.update(data.encode('utf-8'))
    print(m.hexdigest())
    # 原始密码  
    pwd = '123456'  
    # 随机生成4位salt  
    salt = create_salt()  
    # 加密后的密码  
    md5 = create_md5(pwd, salt)  
    
    print('[pwd]\n',pwd ) 
    print('[salt]\n', salt)  
    print('[md5]\n', md5) 

# 获取由4位随机大小写字母、数字组成的salt值  
def create_salt(length = 4):  
    salt = ''  
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'  
    len_chars = len(chars) - 1  
    ran = random.Random()  
    for i in range(length):  
        # 每次从chars中随机取一位  
        salt += chars[ran.randint(0, len_chars)]  
    return salt  
  
# 获取原始密码+salt的md5值  
def create_md5(pwd,salt):  
    md5_obj = hashlib.md5()  
    md5_obj.update((pwd + salt).encode("utf-8"))  
    return md5_obj.hexdigest()
    pass 


if __name__ == "__main__":
    md5_demo()
    pass

