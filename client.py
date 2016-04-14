import socket

'''
print socket.gethostname()
print socket.has_ipv6
print socket.getaddrinfo('www.baidu.com',80)
print socket.gethostbyname_ex('www.google.com')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('',8000))
while True:
    message = raw_input("message is:")
    s.send(message)
    reply = s.recv(1024)
    print 'server said:',reply
s.close()
'''

HOST = ''
PORT = 3212
s = socket.socket()

try:
	s.connect((HOST,PORT))
	data = "hello!"
	while data and data!='q':
		s.sendall(data)
		reply = s.recv(1024)
		print 'received:',reply
		data = raw_input('input your message:')
except socket.error as err:
	print err
finally:
	s.close()


