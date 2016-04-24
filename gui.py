from Tkinter import *
from ttk import *
import threading


from fileServer import BK_PATH,Server

class MyFrame(Frame):

	def __init__(self,root,server):
		Frame.__init__(self,root)
		self.root = root
		self.server = server
		self.grid()

		self.local_ip = self.server.server_local_ip
		self.serv_ports = self.server.server_ports
		self.init_components()

	def init_components(self):
		proj_name = Label(self,text = 'Remote Server')
		proj_name.grid(columnspan = 2)
		
		serv_ip_label = Label(self,text = 'Server Address')
		serv_ip_label.grid(row = 1)

		self.serv_ip = Combobox(self,values = self.server.get_ipaddr())
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

	
	def start_serv(self):
		host = self.serv_ip.get()
		port = int(self.serv_port.get())
		serv_thread = threading.Thread(target = server.start,args = (host,port))
		self.start_btn.state(['disabled',])
		serv_thread.start()

class MyTk(Tk,object):
	#rewrite destroy method
	def __init__(self,server):
		self.server = server
		super(MyTk,self).__init__()

	def destroy(self):
		#terminate the back thread that listening and process port by set SER_RUN_FLAG False
		#global SERRV_RUN_FLAG
		print 'quit server'

		while True:
			if server.flag_lock.acquire():
				self.server.SERRV_RUN_FLAG = False
				server.flag_lock.release()
				break
		Tk.destroy(self)

if __name__ == '__main__':
	server = Server()
	root = MyTk(server)
	root.title('BeiFen server')
	app = MyFrame(root,server)
	app.mainloop()