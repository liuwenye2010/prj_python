#! /usr/bin/python
import hmac
"""
散列消息鉴别码，简称HMAC，是一种基于消息鉴别码MAC（Message Authentication Code）的鉴别机制。使用HMAC时,消息通讯的双方，通过验证消息中加入的鉴别密钥K来鉴别消息的真伪；

一般用于网络通信中消息加密，前提是双方先要约定好key,然后消息发送，用key把消息加密，接收方用key ＋ 消息明文再加密，拿加密后的值 跟 发送者的相对比是否相等，这样就能验证消息的真实性，及发送者的合法性了。

算法表示：

算法公式 ： HMAC（K，M）=H（K⊕opad∣H（K⊕ipad∣M））[1]

H 代表所采用的HASH算法(如SHA-256)

K 代表认证密码

Ko 代表HASH算法的密文

M 代表一个消息输入

B 代表H中所处理的块大小，这个大小是处理块大小，而不是输出hash的大小

如，SHA-1和SHA-256 B = 64

SHA-384和SHA-512 B = 128

L 表示hash的大小

Opad 用0x5c重复B次

Ipad 用0x36重复B次

Apad 用0x878FE1F3重复(L/4)次
  认证流程

(1) 先由客户端向服务器发出一个验证请求。

(2) 服务器接到此请求后生成一个随机数并通过网络传输给客户端 (发起)

(3) 客户端将收到的随机数提供给ePass，由ePass使用该随机数与存储在ePass中的密钥进行HMAC-MD5运算并得到一个结果作为认证证据传给服务器（响应）。

(4) 与此同时，服务器也使用该随机数与存储在服务器数据库中的该客户密钥进行HMAC-MD5运算，如果服务器的运算结果与客户端传回的响应结果相同，则认为客户端是一个合法用户。
"""


def hmac_demo ():
    #set key and message
    h = hmac.new("session_key".encode(encoding="utf-8"),"Message:Hello".encode(encoding="utf-8"))

    #print out the encrypt message
    print(h.hexdigest())


if __name__ == "__main__":
    hmac_demo()
    pass