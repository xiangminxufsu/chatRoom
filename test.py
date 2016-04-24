import threading
import time

def fun():
	print 'fim'
	time.sleep(25.0)


for i in range(6):
	t = threading.Thread(target = fun,)
	t.start()