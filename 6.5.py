import socket
import time

host = ''
port = 5000

clients = []
#this is new line
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

quitting = False
print "Server Started."
while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        if "Quit" in str(data):
            quitting = True
        if addr not in clients:
            clients.append(addr)
            
        print time.ctime(time.time()) + str(addr) + ": :" + str(data)
        for client in clients:
            print client
            print data
            s.sendto(data, client)
    except:
        pass
s.close()


