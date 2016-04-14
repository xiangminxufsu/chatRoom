import socket

HOST = ''
PORT = 3333

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

data = 'hi'

while data:
	s.sendto(data,(HOST,PORT))
	if data == 'q':
		break
	else:
		data,addr = s.recvfrom(1024)
		print 'data,address',data,addr

		data = raw_input('input your message:')
s.close()