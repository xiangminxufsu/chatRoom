from Tkinter import *
from ttk import *
import socket
import struct
import os,pickle
import threading
import time

from comu import BK_PATH,SERRV_RUN_FLAG,flag_lock
from comu.Commu import *

def recv_unit_data(clnt,infos_len):
	data = b''
	while True:
		if infos_len>1024:
			data += clnt.recv(1024)
			infos_len -= 1024
		else:
			data += clnt.recv(infos_len)
			break
	return data

def get_files_info(clnt):
	fmt_str = 'Q'
	headsize = struct.calcsize(fmt_str)
	data = clnt.recv(headsize)
	#print 'data',repr(data)
	infos_len = struct.unpack(fmt_str,data)[0]
	#print 'infos_len',infos_len
	data = recv_unit_data(clnt,infos_len)
	#print 'recv_unit_data',data
	#print pickle.loads(data)
	return pickle.loads(data)

def mk_path(filepath):
	paths = filepath.split(os.path.sep)[:-1]
	p = BK_PATH
	for path in paths:
		p = os.path.join(p,path)
		if not os.path.exists(p):
			os.mkdir(p)

def recv_file(clnt,infos_len,filepath):
	mk_path(filepath)
	filepath = os.path.join(BK_PATH,filepath)
	f = open(filepath,'wb+')

	try:
		if 0<infos_len<=1024:
			data = clnt.recv(infos_len)
			f.write(data)
		else:
			while True:
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
		return True
	finally:
		f.close()

def send_echo(clnt,res):
	if res:
		clnt.sendall(b'success')
	else:
		clnt.sendall(b'')

def client_operate(client):
	files_lst = get_files_info(client)
	print 'files_lst',files_lst
	for size,filepath in files_lst:
		res = recv_file(client,size,filepath)
		print 'res',res
		send_echo(client,res)
	
	client.close()

def start(host,port):
	if not os.path.exists(BK_PATH):
		os.mkdir(BK_PATH)
	st = socket.socket()
	st.bind((host,port))
	st.settimeout(20.0)
	st.listen(5)
	print 'my host and port is ',host,port
	print 'listening'
	#flag_lock.acquire()
	print 'lock acquire'
	while SERRV_RUN_FLAG:
		print 'SERRV_RUN_FLAG',SERRV_RUN_FLAG
		#flag_lock.release()
		time.sleep(2.0)
		client = None
		try:
			client,addr = st.accept()
		except Exception,e:
			print 'eeee',e
			#print 'socket timeout!!!'
			time.sleep(2)
		if client:
			print 'find client'
			t = threading.Thread(target = client_operate,args = (client,))
			t.start()
			#t.join()
			break
		else:
			print 'unable find client'

		#flag_lock.acquire()
	print 'socket closing'
	st.close()

class MyFrame(Frame):

	def __init__(self,root,local_ip,serv_ports):
		Frame.__init__(self,root)
		self.root = root
		self.grid()

		self.local_ip = local_ip
		self.serv_ports = serv_ports
		self.init_components()

	def init_components(self):
		proj_name = Label(self,text = 'Remote Server')
		proj_name.grid(columnspan = 2)
		
		serv_ip_label = Label(self,text = 'Server Address')
		serv_ip_label.grid(row = 1)

		self.serv_ip = Combobox(self,values = dself.get_ipaddr())
		self.serv_ip.set(self.local_ip)
		self.serv_ip.grid(row = 1,column = 1)

		serv_port_label = Label(self,text = 'SERVER PORT')
		serv_port_label.grid(row=2)

		self.serv_port = Combobox(self,values=self.serv_ports)
		self.serv_port.set(self.serv_ports[0])
		self.serv_port.grid(row=2,column=1)

		self.start_btn = Button(self,text = 'Start Server',command=self.start_serv)
		self.start_btn.grid(row=3)

		self.start_exit_bnt = Button(self,text = 'Exit Server',command=self.root.destroy)
		self.start_exit_bnt.grid(row=3,column=1)

	def get_ipaddr(self):
		host_name = socket.gethostname()
		info = socket.gethostbyname_ex(host_name)
		print host_name,info
		info = info[2]
		info.append(self.local_ip)
		print info
		return info
	
	def start_serv(self):
		#print self.serv_ip.get(),self.serv_port.get()
		#start(self.serv_ip.get(),int(self.serv_port.get()))
		host = self.serv_ip.get()
		port = int(self.serv_port.get())
		serv_thread = threading.Thread(target = start,args = (host,port))
		self.start_btn.state(['disabled',])
		serv_thread.start()

class MyTk(Tk):
	def destroy(self):
		global SERRV_RUN_FLAG
		print 'quit server'
		while True:
			if flag_lock.acquire():
				SERRV_RUN_FLAG = False
				flag_lock.release()
				break
		Tk.destroy(self)
		#super(MyTk,self).destroy()

if __name__ == '__main__':
	root = MyTk()
	root.title('BeiFen server')
	local_ip = '127.0.0.1'
	serv_ports = [10887,20888,30888]
	app = MyFrame(root,local_ip,serv_ports)
	app.mainloop()








