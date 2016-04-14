import socket

HOST = ''
PORT = 3333

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST,PORT))

data = True
while data:
	data,addr = s.recvfrom(1024)
	print 'received:',data
	print 'from address:',addr
	s.sendto(data,addr)

s.close()