

from socket import socket, AF_INET, SOCK_STREAM

def writeToScrol(inst):
    print('hi from Queue', inst)
    #client socket
    sock = socket(AF_INET, SOCK_STREAM)
    print("TCP client try to connect to TCP server localhost")
    sock.connect(('localhost', 24000))
    for idx in range(10):
        #client send message to server
        print("Client: send message to server{}".format(idx))
        sock.send(b'Message from a queue: ' + bytes(str(idx).encode()) )
        #client wait recv message from server
        print("Client: wait for reply from {}".format(idx))
        recv = sock.recv(512).decode()
        #Producer : client put message into the queue
        print("Producer: client reply put message into the Queue {}".format(idx))
        inst.guiQueue.put(recv)   
    #trigger thread to process the message from the queue
    print("call inst.createThread(6)")   
    inst.createThread(6)
