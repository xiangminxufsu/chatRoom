import socket
from threading import Thread

HOST = ''
PORT = 3215

s = socket.socket()
s.bind((HOST,PORT))
s.listen(5)

clnt,addr = s.accept()
print ("Client address:",addr)
print 'client is:',clnt

while True:
	data = clnt.recv(1024)
	if not data:
		break
	print ("Receive Data:", data.decode('utf-8'))
	reply = raw_input('input your message:')
	clnt.send(reply)

clnt.close()
s.close()