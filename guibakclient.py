from Tkinter import *
from ttk import *
import socket
import struct
import os,pickle

BK_PATH = 'back'

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

	infos_len = struct.unpack(fmt_str,data)[0]
	data = recv_unit_data(clnt,infos_len)

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
		print e
	else:
		return True
	finally:
		f.close()

def send_echo(clint,res):
	if res:
		clnt.sendall(b'success')
	else:
		clnt.sendall(b'')


def start(host,port):
	if not os.path.exists(BK_PATH):
		os.mkdir(BK_PATH)
		st = socket.socket()
		st.bind((host,port))
		st.listen(1)
		client,addr = st.accept()
		files_lst = get_files_info(client)

		for size,filepath in files_lst:
			res = recv_file(client,size,filepath)
			send_echo(client,res)

		client.close()
		st.close()

class MyFrame(Frame):

	def __init__(self,root):
		Frame.__init__(self,root)
		self.root = root
		self.grid()
		self.remote_ip = '127.0.0.1'
		self.remote_ports = 10888
		self.remote_ip_var = StringVar()
		self.remote_ports_var = IntVar()
		self.bak_src_var = StringVar()
		self.init_components()

	def init_components(self):
		proj_name = Label(self,text = 'Remote Client')
		proj_name.grid(columnspan = 2)
		
		serv_ip_label = Label(self,text = 'Server Address:')
		serv_ip_label.grid(row = 1)

		self.serve_ip = Entry(self,textvariable = self.remote_ip_var)
		self.remote_ip_var.set(self.remote_ip)
		self.serve_ip.grid(row = 1,column = 1)
		print self.remote_ip_var,self.remote_ip_var.get()

		serv_port_label = Label(self,text = 'SERVER PORT')
		serv_port_label.grid(row=2)

		self.serv_port = Entry(self,textvariable = self.remote_ports_var)
		self.remote_ports_var.set(self.remote_ports)
		self.serv_port.grid(row=2,column=1)

		src_label = Label(self,text = 'Target File Path')
		src_label.grid(row=3)

		self.bak_src = Entry(self,textvariable = self.bak_src_var)
		self.bak_src.grid(row=3,column=1)

		self.start_btn = Button(self,text = 'Start BackUP',command=self.start_send)
		self.start_btn.grid(row=4)

		self.start_exit_bnt = Button(self,text = 'Exit Server',command=self.root.destroy)
		self.start_exit_bnt.grid(row=4,column=1)

	def get_ipaddr(self):
		host_name = socket.gethostname()
		info = socket.gethostbyname_ex(host_name)
		info = info[2]
		info.append(self.local_ip)
		print info
		return info
	
	def start_send(self):
		print self.remote_ip_var.get(),self.remote_ports_var.get()
		#start(self.serv_ip.get(),int(self.serv_port.get()))

if __name__ == '__main__':
	root = Tk()
	root.title('BeiFen Client')
	#root.resizeable(False,False)
	app = MyFrame(root)
	app.mainloop()







