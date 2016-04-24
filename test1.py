from test2 import gval,Mythread
import threading,time

class Cm(object):
	def __init__(self):
		pass


class Mythread2(threading.Thread):

	def __init__(self):
		self.gval = 1
		super(Mythread2,self).__init__()

	def run(self):
		global gval
		for i in range(10):
			gval+=1
			print self,gval
			time.sleep(2.0)

ths = [Mythread(),Mythread2()]
#ths = [Mythread() for i in range(3)]
for th in ths:
	th.start()