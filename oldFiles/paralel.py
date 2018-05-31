import time
import multiprocessing


def parallelProcess(myInput):
	while True:
		if not myInput.empty():
			var = myInput.get()
			print('Creating: ',var)
			f = open(str(var),"w")
			f.close()
		

if __name__ == '__main__':
	myInput = multiprocessing.Queue()
	p = multiprocessing.Process(target=parallelProcess,args=(myInput,))
	p.start()
	#e = input('a')
	while True:
		time.sleep(0.1)
		myInput.put(input('Ingrese nombre Archivo: '))
	p.join()