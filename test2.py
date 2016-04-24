import time,threading

gval = 1


class Gval(object):
	def __init__(self):
		

class Mythread(threading.Thread):

	def __init__(self):
		super(Mythread,self).__init__()

	def run(self):
		global gval
		for i in range(10):
			gval+=1
			print self,gval
			time.sleep(2.0)

