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
	print 'data',data
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

def send_echo(clnt,res):
	if res:
		clnt.sendall(b'success')
	else:
		clnt.sendall(b'')


def start(host,port):
	if not os.path.exists(BK_PATH):
		os.mkdir(BK_PATH)
	st = socket.socket()
	st.bind((host,port))
	print 'my host and port is ',host,port
	st.listen(1)
	client,addr = st.accept()
	files_lst = get_files_info(client)

	for size,filepath in files_lst:
		res = recv_file(client,size,filepath)
		send_echo(client,res)

	client.close()
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

		self.serv_ip = Combobox(self,values = self.get_ipaddr())
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
		print self.serv_ip.get(),self.serv_port.get()
		start(self.serv_ip.get(),int(self.serv_port.get()))

if __name__ == '__main__':
	root = Tk()
	root.title('BeiFen server')
	local_ip = '127.0.0.1'
	serv_ports = [10887,20888,30888]
	app = MyFrame(root,local_ip,serv_ports)
	app.mainloop()







