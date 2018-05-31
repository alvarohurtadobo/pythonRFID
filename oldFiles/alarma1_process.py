import MySQLdb, sys, time, datetime, os, smtplib, pygame, signal, smtplib
import RPi.GPIO as GPIO
from threading import Timer
import multiprocessing



alarma = False
acceso = '0'

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN)
GPIO.setup(2, GPIO.IN)
GPIO.setup(4, GPIO.IN)

#Mod Javi
#Funcui de la sql
DB_HOST = '' 
DB_USER = '' 
DB_PASS = '' 
DB_NAME = ''


#client = nexmo.Client(key=3d9b20fa, secret=xfYsPxcZ2Cqlbflt)


def raw_input_with_timeout(prompt, timeout=10.0):
	print (prompt)
	timer = threading.Timer(timeout, _thread.interrupt_main)
	astring = None
	try:
		timer.start()
		astring = input(prompt)
	except KeyboardInterrupt:
		pass
	timer.cancel()
	return astring


TIMEOUT = 10 # number of seconds your want for timeout

def correo():
	fromaddr = ''
	toaddrs  = ''
	msg = 'INFORMACION DE ACTIVIDAD' 
	# Datos
	username = ''
	password = ''
	# Enviando el correo
	server = smtplib.SMTP('smtp.gmail.com')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
	time.sleep(5)

def interrupted(signum, frame):
	
	#"called when read times out"
	print('interrupted!')
	
	
signal.signal(signal.SIGALRM, interrupted)

def run_query(query=''): 
	datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
	conn = MySQLdb.connect(*datos) # Conectar a la base de datos 
	cursor = conn.cursor()         # Crear un cursor 
	cursor.execute(query)          # Ejecutar una consulta 
 
	if query.upper().startswith('SELECT'): 
		data = cursor.fetchall()   # Traer los resultados de un select 
	else: 
		conn.commit()              # Hacer efectiva la escritura de datos 
		data = None 
 
	cursor.close()                 # Cerrar el cursor 
	conn.close()                   # Cerrar la conexión 
	return data


def parallelInput():
	while True:
		myInput.put(input(''))

def rfid():
	
	print('lector_rfid: ')
	if myInput.empty():
		lector_rfid = ''
	else:
		lector_rfid = myInput.get()
	#lector_rfid = input("lector_rfid: ")

##    t = Timer(TIMEOUT, print, ['Sorry, times up \n \n'])
##    t.start()
##    
##    lector_rfid = input("lector_rfid: ")
##    print('rrrrrr')
##    t.exit()
##
##    t.cancel()

	# disable the alarm after success
	query = "SELECT n_tarjeta, n_pin FROM usuaris WHERE n_tarjeta = '%s'" % lector_rfid
	try:
		result = run_query(query) #Trucada a la funcio run_query
	except:
		print ("ERROR")
	print (result) #Mostra reslutats de la funcio
	llista_usuaris = result
	for usuari in llista_usuaris:
		print(usuari[0])
		print(usuari[1])
		if str(lector_rfid) == str(usuari[0]):
			print("KKKKK")
			return True
	return False
	

def input_timeout():
	try:
		print('You have 5 seconds to type in your stuff...')
		return input("Ingrese la tarjeta RFID: ")
	except:
		# timeout
		return "timeout"
	
	

	
def main():
	print("PROGRAMA INCIADO CORRECTAMANETE")
	print(alarma)
	acceso_permitido = False

	while True:
		if GPIO.input(3) == False and acceso_permitido == False:
			print("DETECIO INSTANTANEA DE MOVIMENT ZONA1")
			#Timeout 10segons posar PIN
			
			#acceso_permitido = rfid()
			print(time.strftime("%H:%M:%S")) #Despues posarem un registre a la sql
			if acceso_permitido == False:
				print("ALARMA!!!!!")
		elif GPIO.input(2) == False and acceso_permitido == False:
			print("MOVIMENT ZONA2 EN 15 SEG SALTARA LA ALARMA ")
			time.sleep(1.5)
			
			acceso_permitido = rfid()
		elif GPIO.input(4) == True and acceso_permitido == False:
			print("salto de zona 2")
		else:
			pass
		
						 
		print('Accesso: ', acceso_permitido)
		
		time.sleep(1.5)



if __name__ == "__main__":
	global myInput
	myInput = multiprocessing.Queue()
	captura = multiprocessing.Process(target=parallelInput)
	main()    
	
	
	


		
				
			
					