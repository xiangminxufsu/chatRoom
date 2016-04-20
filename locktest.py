import threading,os,time

share = 0
share_cond = threading.Condition()

class Produce(threading.Thread):
	def __init__(self):
		super(Produce,self).__init__()

	def run(self):
		global share
		while True:
			#if share<=0:

			if share_cond.acquire():
				print 'Produce acquired'
				share_cond.wait()
				print 'wait ended'
				'''
				time.sleep(5)
				if share<=0:
					share+=2
					print 'share is now', share
				time.sleep(5)
				share_cond.notify()
				print 'Produce notify'
				print 'Produce wait'
				share_cond.wait()
				print 'Produce wiat ended'
				time.sleep(3)
				'''

class Customer(threading.Thread):
	def __init__(self):
		super(Customer,self).__init__()

	def run(self):
		global share
		while True:
			#if share>0:
			if share_cond.acquire():
				print 'Customer acquired'
				share_cond.notify()
				print 'notify'
				'''
				while share>0:
					share -= 1
					print 'share val is', share
				share_cond.notify()
				print 'Customer notify'
				print 'Customer wait'
				share_cond.wait()
				print 'Customer wiat ended'
				time.sleep(3)
				'''
if __name__ == '__main__':
	t = Produce()
	tt = Customer()
	t.start()
	tt.start()
	
			
			