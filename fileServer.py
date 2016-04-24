import socket
import struct
import os,pickle
import threading
import time

BK_PATH = 'back'
#SERRV_RUN_FLAG = True
#flag_lock = threading.Lock()



class Server(object):

	def __init__(self):
		self.local_ip = '127.0.0.1'
		self.serv_ports = [10887,20888,30888]
		self.SERRV_RUN_FLAG = True
		self.flag_lock = threading.Lock()

	@property
	def server_local_ip(self):
		return self.local_ip

	@property
	def server_ports(self):
		return self.serv_ports

	def recv_unit_data(self,clnt,infos_len):
		data = b''
		while True:
			if infos_len>1024:
				data += clnt.recv(1024)
				infos_len -= 1024
			else:
				data += clnt.recv(infos_len)
				break
		return data

	def get_files_info(self,clnt):
		fmt_str = 'Q'
		headsize = struct.calcsize(fmt_str)
		data = clnt.recv(headsize)
		#print 'data',repr(data)
		infos_len = struct.unpack(fmt_str,data)[0]
		#print 'infos_len',infos_len
		data = self.recv_unit_data(clnt,infos_len)
		#print 'recv_unit_data',data
		print pickle.loads(data)
		return pickle.loads(data)

	def mk_path(self,filepath):
		paths = filepath.split(os.path.sep)[:-1]
		p = BK_PATH
		for path in paths:
			p = os.path.join(p,path)
			if not os.path.exists(p):
				os.mkdir(p)

	def recv_file(self,clnt,infos_len,filepath):
		print 'infos_len,filepath:',infos_len,filepath
		self.mk_path(filepath)
		filepath = os.path.join(BK_PATH,filepath)
		f = open(filepath,'wb+')

		try:
			while True:
				print infos_len,clnt
				if infos_len >1024:
					data = clnt.recv(1024)
					f.write(data)
					infos_len -= 1024
				else:
					data = clnt.recv(infos_len)
					f.write(data)
					break
		except Exception,e:
			print 'e is here'
			print e
		else:
			print 'receive file'
			return True
		finally:
			f.close()

	def send_echo(self,clnt,res):
		if res:
			clnt.sendall(b'success')
		else:
			clnt.sendall(b'')

	def client_operate(self,client):
		files_lst = self.get_files_info(client)
		#print 'files_lst',files_lst
		for size,filepath in files_lst:
			res = self.recv_file(client,size,filepath)
			self.send_echo(client,res)
		
		client.close()

	@staticmethod
	def get_ipaddr():
		host_name = socket.gethostname()
		info = socket.gethostbyname_ex(host_name)
		print 'local server and info:',host_name,info
		info = info[2]
		#info.append(cls.local_ip)
		return info

	def start(self,host,port):
		print 'receive start server command!'
		if not os.path.exists(BK_PATH):
			os.mkdir(BK_PATH)

		st = socket.socket()
		st.bind((host,port))
		st.settimeout(2.0)
		st.listen(5)

		print 'my host and port is ',host,port
		print 'listening'
		self.flag_lock.acquire()
		print 'lock acquire'
		while self.SERRV_RUN_FLAG:
			print 'SERRV_RUN_FLAG',self.SERRV_RUN_FLAG
			self.flag_lock.release()
			client = None
			try:
				client,addr = st.accept()
				client.setblocking(1)
			except Exception,e:
				print 'eeee',e
			if client:
				print 'find client'
				t = threading.Thread(target = self.client_operate,args = (client,))
				t.start()
				t.join()
			self.flag_lock.acquire()
		print 'socket closing'
		st.close()

