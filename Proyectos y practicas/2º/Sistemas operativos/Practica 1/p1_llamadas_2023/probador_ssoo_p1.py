'''
Alberto Garcia Fernandez

Sistemas Operativos - Practica 1 - Llamadas al sistema

Este programa verifica que el formato del entregable de la practica es el correcto (sigue las especificaciones de nombrado, y esta bien comprimido).

Tambien realiza una prueba basica de funcionamiento para cada uno de los tres programas solicitados en la practica. Cumplir esta prueba no es garantia de tener la maxima nota en el ejercicio. Se trata solo de una sugerencia para que los alumnos comprueben el funcionamiento general de su programa. Los alumnos deberan ademas cumplir los otros requisitos del programa, realizar el codigo adecuado, comentarlo, probar casos extremos, y en general cumplir con las demas exigencias descritas en el enunciado de la practica. El programa crea un entorno de prueba en la carpeta /tmp/ssoo/ y crea los siguientes objetos:

Directorio dirC
Directorio dirA
Fichero f_empty.txt (vacio)
Fichero	f_aes.txt (contiene "AAAAA")
Copia de los ficheros fuente del alumno.
Ejecutables compilados a partir de los ficheros fuente del alumno.

Con todos estos objetos, realiza pruebas basicas del mywc, myls y myenv
'''
import subprocess
import signal
import os
import glob
import time
import sys

resultString=""
result=0

def normalizeOutput(result):
	'''
	Funcion que normaliza una cadena de entrada con el fin de eliminar errores de formato. Reemplaza saltos de linea por tabuladores y elimina espacios repetidos y espacios al principio y final
	'''

	result = result.decode('ascii')

	result = result.replace("\r\n","\n");
	result = result.replace("\r","\n");
	resultList = result.split("\n")
	resultNormalized = ""
	for resultLine in resultList:
		if resultLine == "":
			continue
		resultLine = resultLine.replace("\t", " ")
		resultLine = resultLine.replace("  ", " ")
		resultLine = resultLine.strip()
		resultNormalized += (resultLine + "\t")

	resultNormalized = resultNormalized.strip()

	return resultNormalized


def lookForTargetFile(folder,targetFile):
	'''
	Funcion que busca un fichero objetivo en una carpeta y devuelve su ruta
	'''
	toReturn="-"
	found=False
	subfolders=[x[0] for x in os.walk(folder)]
	for innerFolder in subfolders:
		folders=os.listdir(innerFolder)
		for item in folders:
			if item.lower()==targetFile.lower():
				return innerFolder+"/"+item
	return toReturn
	

def checkTargetFile(folder,targetFile):
	'''
	Funcion que comprueba que un fichero objetivo existe. Si no existe, lo intenta buscar en las carpetas hijas.
	'''
	toReturn="-"
	filePath=folder+targetFile
	if not os.path.exists(filePath):
		toReturn=lookForTargetFile(folder,targetFile)
	else:
		toReturn=filePath
	return toReturn



def testExerciseWC(folder):
	'''
	Funcion que realiza la prueba sugerida del programa mywc
	'''

	global resultString 
	global result
	global minipunto
	#Definimos los nombres del fichero de codigo fuente, programa y fichero de prueba
	targetFile="mywc.c"
	programFile="mywc"
	
	#Buscamos el fichero fuente
	filePath=checkTargetFile(folder,targetFile)
	if filePath=="-":
		print ("CHECKER:", targetFile, "not found")
		return "-"
	
	#Compilamos el fichero fuente
	programPath=folder+programFile
	compiled=subprocess.call(["gcc", filePath,"-o", programPath])
	if compiled != 0:
		print ("CHECKER:", "Compile error", targetFile)
		return "-"

	#Realizamos la prueba sugerida (wc <fichero>)
	result1 = subprocess.check_output(["wc", folder+testFile])

	#Ejecutamos el programa del alumno
	cmd = programPath + " " + folder+testFile
	pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, preexec_fn=os.setsid)  
	time.sleep(0.5)
	os.killpg(pro.pid, signal.SIGTERM) 

	result2, stderr = pro.communicate()

	#Obtenemos las salidas de la prueba con la que vamos a comparar y de la ejecucion del programa del alumno
	expectedResult = normalizeOutput(result1)
	obtainedResult = normalizeOutput(result2)

	#Comparamos las salidas e imprimimos resultados
	print ("MYWC CHECKER. Expected output:")
	print (result1.decode('ascii'))
	print ("MYWC CHECKER. Program output:") 
	print (result2.decode('ascii'))

	if result1 == result2:
		print ("MYWC CHECKER. CORRECT TEST")
		resultString += "1 " 
		result += 0.9091
	else:
		print ("MYWC CHECKER. INCORRECT TEST. Outputs differ")
		resultString += "0 "


	#Realizamos la prueba sugerida (wc <fichero empty>)
	result1 = subprocess.check_output(["wc", folder+"f_empty.txt"])

	#Ejecutamos el programa del alumno
	cmd = programPath + " " + folder+"f_empty.txt"
	pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	time.sleep(0.5)
	os.killpg(pro.pid, signal.SIGTERM)

	result2, stderr = pro.communicate()

	#Obtenemos las salidas de la prueba con la que vamos a comparar y de la ejecucion del programa del alumno
	expectedResult = normalizeOutput(result1)
	obtainedResult = normalizeOutput(result2)

	#Comparamos las salidas e imprimimos resultados
	print ("MYWC CHECKER. Expected output:")
	print (result1.decode('ascii'))
	print ("MYWC CHECKER. Program output:")
	print (result2.decode('ascii'))

	if result1 == result2:
		print ("MYWC CHECKER. CORRECT TEST")
		resultString += "1 "
		result += 0.9091
	else:
		print ("MYWC CHECKER. INCORRECT TEST. Outputs differ")
		resultString += "0 "


	#Realizamos la prueba sugerida (wc <fichero que no existe>)
	result1 = 255

	#Ejecutamos el programa del alumno
	cmd = programPath + " " + folder+"notfound.txt"
	pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	time.sleep(0.5)
	os.killpg(pro.pid, signal.SIGTERM)

	result2, stderr = pro.communicate()
	result2 = pro.returncode

	#Comparamos las salidas e imprimimos resultados
	print ("MYWC CHECKER. Expected output:")
	print (result1)
	print ("MYWC CHECKER. Program output:" )
	print (result2)

	if result1 == result2:
		print ("MYWC CHECKER. CORRECT TEST")
		resultString += "1 "
		result += 0.9091
	else:
		print ("MYWC CHECKER. INCORRECT TEST. Outputs differ")
		resultString += "0 "
	#Realizamos la prueba sugerida (wc nofile)
	result1 = 255

	#Ejecutamos el programa del alumno
	cmd = programPath 
	pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	time.sleep(0.5)
	os.killpg(pro.pid, signal.SIGTERM)

	result2, stderr = pro.communicate()
	result2 = pro.returncode

	#Comparamos las salidas e imprimimos resultados
	print ("MYWC CHECKER. Expected output:")
	print (result1)
	print ("MYWC CHECKER. Program output:" )
	print (result2)

	if result1 == result2:
		print ("MYWC CHECKER. CORRECT TEST")
		resultString += "1 "
		result += 0.9091
	else:
		print ("MYWC CHECKER. INCORRECT TEST. Outputs differ")
		resultString += "0 "


def testExerciseENV(folder):
	'''
	Funcion que realiza la prueba sugerida del programa myenv
	'''

	global resultString 
	global result
	global minipunto
	#Definimos los nombres del fichero de codigo fuente, programa y fichero de prueba
	targetFile="myenv.c"
	programFile="myenv"
	
	#Buscamos el fichero fuente
	filePath=checkTargetFile(folder,targetFile)
	if filePath=="-":
		print ("CHECKER:", targetFile, "not found")
		return "-"
	
	#Compilamos el fichero fuente
	programPath=folder+programFile
	compiled=subprocess.call(["gcc", filePath,"-o", programPath])
	if compiled != 0:
		print ("CHECKER:", "Compile error", targetFile)
		return "-"

	#Realizamos la prueba sugerida (grep SHELL env.txt)
	result1 = subprocess.check_output(["grep","SHELL", folder+"env.txt"])

	#Ejecutamos el programa del alumno
	os.chdir(folder)
	cmd = programPath + " SHELL myenv_output.txt"
	pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, preexec_fn=os.setsid)  
	time.sleep(0.5)
	os.killpg(pro.pid, signal.SIGTERM)

	if os.path.exists("myenv_output.txt"):

		result2 = subprocess.check_output(["cat","myenv_output.txt"])

		#Obtenemos las salidas de la prueba con la que vamos a comparar y de la ejecucion del programa del alumno
		expectedResult = normalizeOutput(result1)
		obtainedResult = normalizeOutput(result2)

		#Comparamos las salidas e imprimimos resultados
		print ("MYENV CHECKER. Expected output:")
		print (result1.decode('ascii'))
		print ("MYENV CHECKER. Program output:") 
		print (result2.decode('ascii'))

		if result1 == result2:
			print ("MYENV CHECKER. CORRECT TEST")
			resultString += "1 " 
			result += 0.9091
		else:
			print ("MYENV CHECKER. INCORRECT TEST. Outputs differ")
			resultString += "0 "

	else:
		print ("MYENV CHECKER. INCORRECT TEST. Outputs differ")
		resultString += "0 "

	
	#Realizamos la prueba sugerida (grep UTF-8 env.txt)
	#result1 = subprocess.check_output(["grep","UTF-8",folder+"env.txt"])
	result1 = b''

	#Ejecutamos el programa del alumno
	os.chdir(folder)
	cmd = programPath + " UTF-8 myenv_output.txt"
	pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	time.sleep(0.5)
	os.killpg(pro.pid, signal.SIGTERM)

	if os.path.exists("myenv_output.txt"):

		result2 = subprocess.check_output(["cat","myenv_output.txt"])

		#Obtenemos las salidas de la prueba con la que vamos a comparar y de la ejecucion del programa del alumno
		expectedResult = normalizeOutput(result1)
		obtainedResult = normalizeOutput(result2)

		#Comparamos las salidas e imprimimos resultados
		print ("MYENV CHECKER. Expected output:")
		print (result1.decode('ascii'))
		print ("MYENV CHECKER. Program output:")
		print (result2.decode('ascii'))

		if result1 == result2:
			print ("MYENV CHECKER. CORRECT TEST")
			resultString += "1 "
			result += 0.9091
		else:
			print ("MYENV CHECKER. INCORRECT TEST. Outputs differ")
			resultString += "0 "
	else:
		print ("MYENV CHECKER. INCORRECT TEST. Outputs differ")
		resultString += "0 "

	
	#Realizamos la prueba sugerida (grep NOTEXIST env.txt)
	#result1 = subprocess.check_output(["grep","NOTEXIST",folder+"env.txt"])
	result1 = b''

	#Ejecutamos el programa del alumno
	cmd = programPath + " NOTEXIST myenv_output.txt"
	pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	time.sleep(0.5)
	os.killpg(pro.pid, signal.SIGTERM)

	if os.path.exists("myenv_output.txt"):

		result2 = subprocess.check_output(["cat","myenv_output.txt"])

		#Obtenemos las salidas de la prueba con la que vamos a comparar y de la ejecucion del programa del alumno
		expectedResult = normalizeOutput(result1)
		obtainedResult = normalizeOutput(result2)

		#Comparamos las salidas e imprimimos resultados
		print ("MYENV CHECKER. Expected output:")
		print (result1.decode('ascii'))
		print ("MYENV CHECKER. Program output:")
		print (result2.decode('ascii'))

		if result1 == result2:
			print ("MYENV CHECKER. CORRECT TEST")
			resultString += "1 "
			result += 0.9091
		else:
			print ("MYENV CHECKER. INCORRECT TEST. Outputs differ")
			resultString += "0 "
	else:
		print ("MYENV CHECKER. INCORRECT TEST. Outputs differ")
		resultString += "0 "


	#Realizamos la prueba sugerida (wc nofile)
	result1 = 255

	#Ejecutamos el programa del alumno
	cmd = programPath 
	pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	time.sleep(0.5)
	os.killpg(pro.pid, signal.SIGTERM)

	result2, stderr = pro.communicate()
	result2 = pro.returncode

	#Comparamos las salidas e imprimimos resultados
	print ("MYENV CHECKER. Expected output:")
	print (result1)
	print ("MYENV CHECKER. Program output:" )
	print (result2)

	if result1 == result2:
		print ("MYENV CHECKER. CORRECT TEST")
		resultString += "1 "
		result += 0.9091
	else:
		print ("MYENV CHECKER. INCORRECT TEST. Outputs differ")
		resultString += "0 "


def testExerciseLS(folder):
	'''
	Funcion que realiza la prueba sugerida del programa myls
	'''
	global resultString
	global result
	global minipunto
	#Definimos los nombres del fichero de codigo fuente y programa
	targetFile="myls.c"
	programFile="myls"

	#Buscamos el fichero fuente
	filePath=checkTargetFile(folder,targetFile)
	if filePath=="-":
		print ("CHECKER:", targetFile, "not found")
		return "-"

	#Compilamos el fichero fuente
	programPath=folder+programFile
	compiled=subprocess.call(["gcc", filePath,"-o", programPath])
	if compiled != 0:
		print ("CHECKER:", "Compiler error", targetFile)
		return "-"

	#Realizamos la prueba sugerida (ls -f1 <carpeta>)
	result1 = subprocess.check_output(["ls","-f1",folder])

	#Ejecutamos el programa del alumno
	cmd = programPath + " " + folder
	pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, preexec_fn=os.setsid)  
	time.sleep(0.5)
	os.killpg(pro.pid, signal.SIGTERM) 
	result2, stderr = pro.communicate()

	#Obtenemos las salidas de la prueba con la que vamos a comparar y de la ejecucion del programa del alumno
	expectedResult = normalizeOutput(result1)
	obtainedResult = normalizeOutput(result2)

	#Comparamos las salidas e imprimimos resultados
	print ("MYLS CHECKER. Expected output:" )
	print (result1.decode('ascii'))
	print ("MYLS CHECKER. Program output:" )
	print (result2.decode('ascii'))

	if result1 == result2:
		print ("MYLS CHECKER. CORRECT TEST")
		resultString += "1 "
		result += 0.9091
	else:
		print ("MYLS CHECKER. INCORRECT TEST. Outputs differ")
		resultString += "0 "


	#Realizamos la prueba sugerida (ls -f -1 nothing)
	result1 = subprocess.check_output(["ls","-f1"])

	#Ejecutamos el programa del alumno
	cmd = programPath
	pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	time.sleep(0.5)
	os.killpg(pro.pid, signal.SIGTERM)
	result2, stderr = pro.communicate()

	#Obtenemos las salidas de la prueba con la que vamos a comparar y de la ejecucion del programa del alumno
	expectedResult = normalizeOutput(result1)
	obtainedResult = normalizeOutput(result2)

	#Comparamos las salidas e imprimimos resultados
	print ("MYLS CHECKER. Expected output:" )
	print (result1.decode('ascii'))
	print ("MYLS CHECKER. Program output:" )
	print (result2.decode('ascii'))

	if result1 == result2:
		print ("MYLS CHECKER. CORRECT TEST")
		resultString += "1 "
		result += 0.9091
	else:
		print ("MYLS CHECKER. INCORRECT TEST. Outputs differ")
		resultString += "0 "


	#Realizamos la prueba sugerida (ls -f -1 nothing)
	result1 = 255

	#Ejecutamos el programa del alumno
	cmd = programPath+" directory not found"
	pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
	time.sleep(0.5)
	os.killpg(pro.pid, signal.SIGTERM)
	result2, stderr = pro.communicate()
	result2 = pro.returncode
	#Obtenemos las salidas de la prueba con la que vamos a comparar y de la ejecucion del programa del alumno

	#Comparamos las salidas e imprimimos resultados
	print ("MYLS CHECKER. Expected output:")
	print (result1)
	print ("MYLS CHECKER. Program output:" )
	print (result2)

	if result1 == result2:
		print ("MYLS CHECKER. CORRECT TEST")
		resultString += "1 "
		result += 0.9091
	else:
		print ("MYLS CHECKER. INCORRECT TEST. Outputs differ")
		resultString += "0 "



if(__name__=="__main__"):
	'''
	Funcion main de la aplicacion. Obtiene el fichero pasado como argumento. Lo descomprime, chequea su formato y finalmente lanza las pruebas.
	'''

	if (sys.version_info[0] < 3):
		print ('ERROR: Python3 must be used\n\tpython3 probador_ssoo_p1.py <entregable.zip>')
		sys.exit(0)

	#Comprobamos que se ha pasado un fichero como argumento
	if not len(sys.argv) == 2:
		print ('Uso: python3 probador_ssoo_p1.py <entregable.zip>')
	else:
		print ('CHECKER: correcting', sys.argv[1])
		inputFile = sys.argv[1]
		
		#Comprobamos que el fichero existe
		if not os.path.isfile(inputFile):
			print ("The file", inputFile, "does not exist")
			sys.exit(0)
	
		#Comprobamos el formato del nombre del fichero
		tokens=inputFile.replace(".zip","")
		tokens=tokens.split("_")
		if len(tokens) != 3 and len(tokens) != 4 and len(tokens) != 5:
			print ("Incorrect file name format: ssoo_p1_AAAAA_BBBBB_CCCCC.zip")
			sys.exit(0)
			
		ssoo=tokens[0]
		p1=tokens[1]
		u1=tokens[2]
		u2=""
		u3=""
		if len(tokens)>3:
			u2=tokens[3]
			if len(tokens)>4:
				u3=tokens[4]
		if not (ssoo == "ssoo" and p1 == "p1"):
			print ("Incorrect file name format: ssoo_p1_AAAAA_BBBBB_CCCCC.zip")
			sys.exit(0)

		print ("CHECKER: NIA 1",u1, "NIA 2", u2, "NIA 3", u3)
		
		#Preparamos la carpeta temporal donde se realizaran las pruebas
		tempFolder="/tmp/os/"
		testFile="f_aes.txt"
		if os.path.exists(tempFolder):
			subprocess.call(["rm", "-r",tempFolder])

		os.mkdir(tempFolder)
		os.mkdir(tempFolder+"dirC")
		os.mkdir(tempFolder+"dirA")

		subprocess.call(["touch",tempFolder+"f_empty.txt"])		
		subprocess.call("echo -n \"AAAAA\" > " + tempFolder + testFile, shell=True)
		
		subprocess.call(["cp",inputFile,tempFolder])
		subprocess.call(["touch",tempFolder+"dirA/"+"f_sizetrue.txt"])
		subprocess.call("echo -n \"AAAAA\" > " + tempFolder + testFile, shell=True)

		#Prepare a env file
		#subprocess.call("env > " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"SHELL=/bin/bash\" > " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LC_ADDRESS=es_ES.UTF-8\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LC_NAME=es_ES.UTF-8\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LC_MONETARY=es_ES.UTF-8\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"PWD=/home/profes/ssoo-uc3m\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LOGNAME=ssoo-uc3m\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"XDG_SESSION_TYPE=tty\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"MOTD_SHOWN=pam\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"HOME=/home/profes/ssoo-uc3m\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LANG=es_ES.UTF-8\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LC_PAPER=es_ES.UTF-8\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.webp=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"SSH_CONNECTION=127.0.0.1 44 127.0.0.1 22\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"XDG_SESSION_CLASS=user\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"TERM=xterm-256color\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LC_IDENTIFICATION=es_ES.UTF-8\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"USER=ssoo-uc3m\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"SHLVL=1\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LC_TELEPHONE=es_ES.UTF-8\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LC_MEASUREMENT=es_ES.UTF-8\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"XDG_SESSION_ID=c114\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"XDG_RUNTIME_DIR=/run/user/1234\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"SSH_CLIENT=127.0.0.1 44 22\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LC_TIME=es_ES.UTF-8\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"XDG_DATA_DIRS=/usr/local/share:/usr/share:/var/lib/snapd/desktop\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/snap/bin\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1234/bus\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"SSH_TTY=/dev/pts/0\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"LC_NUMERIC=es_ES.UTF-8\" >> " + tempFolder + "env.txt", shell=True)
		subprocess.call("echo \"_=/usr/bin/env\" >> " + tempFolder + "env.txt", shell=True)

		print ('CHECKER: decompressing')

		#Descomprimimos el fichero en la carpeta temporal
		zipresult=subprocess.call(["unzip",tempFolder+"*.zip","-d",tempFolder])
		if not zipresult == 0:
			print ("Error decompressing zip file")
			sys.exit(0)
		
		#Comprobamos que el fichero de autores existe
		if not os.path.isfile(tempFolder+"autores.txt"):
			print ("The file autores.txt does not exist")
			sys.exit(0)

		
		#Realizamos una prueba basica de cada uno de los programas

		testExerciseWC(tempFolder)

		testExerciseENV(tempFolder)

		testExerciseLS(tempFolder)

		resultString
		print(resultString) 
		result
		print ("Nota: ", result)
		subprocess.call("echo " + str(result) + "> nota.txt", shell=True)
		