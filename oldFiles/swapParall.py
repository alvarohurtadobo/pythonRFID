import time
import multiprocessing


def parallelProcess(myInput):
	while True:
		time.sleep(0.1)
		myInput.put(input('Ingrese nombre Archivo: '))
		

if __name__ == '__main__':
	myInput = multiprocessing.Queue()
	p = multiprocessing.Process(target=parallelProcess,args=(myInput,))
	p.start()
	#e = input('a')
	while True:
		if not myInput.empty():
			f = open(str(myInput.get()),"w")
			f.close()
	p.join()