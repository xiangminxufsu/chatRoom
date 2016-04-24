from Tkinter import *
from ttk import *
import socket
import struct
import os,pickle

#BK_PATH = 'back'
#added a new line too!
def get_files_info(path):
	if not path or not os.path.exists(path):
		return None
	files = os.walk(path)
	infos = []
	file_paths = []

	for p,ds,fs in files:
		#print p,ds,fs
		for f in fs:
			file_name = os.path.join(p,f)
			file_size = os.stat(file_name).st_size
			file_paths.append(file_name)
			file_name = file_name[len(path)+1:]
			infos.append((file_size,file_name))
	#print infos,file_paths
	return infos,file_paths

def send_files_infos(my_sock,file_infos):
	fmt_str = 'Q'
	infos_bytes = pickle.dumps(file_infos)
	#print 'infos_bytes',infos_bytes
	infos_bytes_len = len(infos_bytes)
	#print 'infos_bytes_len',infos_bytes_len
	infos_len_pack = struct.pack(fmt_str,infos_bytes_len)
	print 'infos_len_pack',repr(infos_len_pack),(infos_len_pack)
	my_sock.sendall(infos_len_pack)
	my_sock.sendall(infos_bytes)

def send_files(my_sock,file_path):
	f = open(file_path,'rb')
	try:
		while True:
			data = f.read(1024)
			if data:
				my_sock.sendall(data)
			else:
				break
	finally:
		f.close()

def get_bak_info(my_sock,size=7):
	info = my_sock.recv(size)
	print info.decode('utf-8')

def start(host,port,src):
	if not os.path.exists(src):
		print 'backup file not exists'
		return 
	path = src
	file_infos,file_paths = get_files_info(path)
	s = socket.socket()
	s.connect((host,port))
	#file_infos,file_paths = get_files_info(path)
	#print 'file_infos,file_paths',file_infos,file_paths
	send_files_infos(s,file_infos)
	#print file_paths
	#file_paths.sort()
	#print 'after',file_paths
	for fp in file_paths:
		send_files(s,fp)
		print fp
		get_bak_info(s)
	s.close()

class MyFrame(Frame):

	def __init__(self,root):
		Frame.__init__(self,root)
		self.root = root
		self.grid()
		self.remote_ip = '127.0.0.1'
		self.remote_ports = 10887
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
		start(self.remote_ip_var.get(),int(self.remote_ports_var.get()),self.bak_src_var.get())

if __name__ == '__main__':
	root = Tk()
	root.title('BeiFen Client')
	#root.resizeable(False,False)
	app = MyFrame(root)
	app.mainloop()



#/Users/xx12b/Project/chatRoom/sample



