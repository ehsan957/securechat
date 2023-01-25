import socket
import threading
import random
import time
port = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket = None
isServer = False
ip = "192.168.10.79"
xor = 0
def crypt(bs):
    xor = 10
    rst = []
    for b in bs:
        rst.append(b^xor)
    return bytes(rst)
def infinite_recieve(isServer, s, clientsocket):
    while True:
        if isServer:
            msg = clientsocket.recv(1024)
        else:
            msg = s.recv(1024)
        if len(msg)>0:
            if msg.decode()[0:3] == "@@@":
                xor = int(msg.decode()[3:5])
            else:
                msg = crypt(msg)
                print(msg.decode())
def infinite_send(isServer, s , clientsocket):
    while True:
        t = int(time.time())
        if t % 30 == 0:
            xor = random.randint(10,100)
            clientsocket.send(("@@@"+str(xor)).encode())
            continue
        else:
            msg = input()
        if isServer:
            msg = clientsocket.send(crypt(msg.encode()))
        else:
            s.send(crypt(msg.encode()))
try:
    ip = input("Please enter IP of your friend: ")
    s.connect((ip, port))
except:
    s = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", port))
    s.listen(1)
    print("I am a server")
    isServer = True
    while True:
        clientsocket, address = s.accept()
        break
else:
    print("I am a client")
finally:
    thread1 = threading.Thread(target=infinite_recieve, args=[isServer, s, clientsocket])
    thread1.start()

    thread2 = threading.Thread(target=infinite_send, args=[isServer, s, clientsocket])
    thread2.start()
    if isServer:
        xor = random.randint(10,100)
        clientsocket.send(("@@@"+str(xor)).encode())

