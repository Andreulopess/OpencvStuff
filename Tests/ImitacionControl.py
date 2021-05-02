# -*- coding: Windows-1252 -*-
# -*- coding: cp1252 -*-
# -*- coding: utf-8 -*-
# -*- coding: IBM850 -*
from naoqi import ALProxy
import cv2
import numpy as np
import imutils
import time
import argparse
import subprocess
import qi
from PIL import Image
import math
import gettext
from random import choice


#Great job, good job, that's cool

#-------------------------------------DEFINICI0N DE VARIABLES----------------
photo_taken = False
archivo = "image.png"
cascPath = "haarcascade_frontalface_default.xml"
x = 0
y = 0
cara_x = 0
cara_y = 0
cara = True
final = False

#Rangos de colores en HSV a detectar
loweryellow = [18, 100, 100]
upperyellow = [30, 255, 255]
lowergreen = [80,80,50]
uppergreen = [100,255,255]
lowerlightgreen = [40, 100, 50]
upperlightgreen = [75, 255, 255]

#Parser para pasarle argumentos
parser = argparse.ArgumentParser()
parser.add_argument('user',action="store", type = str)
parser.add_argument('sesion', action="store", type =int)
parser.add_argument('np', help="nos apunta a la postura con la que queremos jugar",type=int)
parser.add_argument('-i',"--init", action="store", type=int, default =0)
parser.add_argument('-s',"--silla", action="store", type=int, default =0)
parser.add_argument('-f',"--fallos", action="store", type=int, default =0)
args = parser.parse_args()





#Guardamos los argumentos
nextposture = args.np
user = args.user
sesion = args.sesion
#Opcional, solo nos dice si hacemos presentación o no
init = args.init
#Opcional, nos dice si el jugador va en silla de ruedas o no
silla = args.silla
#opcional, nos dice cuántos fallos lleva
fallos = args.fallos


if init==1:
	pres = True;
else:
	pres = False;


#Parámetros conexiones con NAO
port = 9559
ip = "NAO2018.local"
tts = ALProxy("ALTextToSpeech",ip,port)
tts.setLanguage("Spanish")
p = ALProxy("ALBehaviorManager",ip,port)
ruta = "emote/data/"+user+"/"+str(sesion)
file_name = ruta+"/data.txt"


#------------------------------------DEFINICI0N DE METODOS-----------------
#Definimos el orden del juego y su lógica
def presentacion():
	tts.say('Hola ' +user + " soy NAO y estoy aquí para ayudarte con tu sesión de rehabilitación. Tienes que imitarme como si fuera un espejo a lo largo del ejercicio.")
	tts.say('Recuerda que mientras hagas el movimiento, tienes que mirarme a los ojos')
	tts.say('Hoy, vamos a entrenar tu tren superior ' +user + '. Vamos a ejercitar tus brazos para mejorar su movilidad.')
#Definimos el orden del juego y su lógica
def game_logic():
	#Selecciona el orden del juego
	global nextposture
	global final
	if nextposture == 1:
		p.startBehavior("brazosarriba-4ca04c/macarena")
		time.sleep(4)
		tts.say(("¡Alza las dos palmas de las manos lo más alto que puedas!"))
		tts.say(("Igual que lo hago yo"))
	elif nextposture == 3:
		p.startBehavior("brazoabajos-690394/macarena")
		time.sleep(4)

		if silla > 0:
			tts.say(("Ahora vamos a relajarnos, deja los dos brazos sobre tus piernas, sin hacer fuerza."))
		else:
			tts.say(("Ahora vamos a relajarnos, deja los dos brazos muertos abajo, sin hacer fuerza."))
	elif nextposture == 2:
		p.startBehavior("derecho-794efe/macarena")
		time.sleep(4)
		tts.say(("Venga vamos, ahora alza la mano izquierda lo más alto que puedas. Estoy orgulloso de ti!"))
	elif nextposture == 4:
		p.startBehavior("izquierdo-863d90/macarena")
		time.sleep(4)
		if silla > 0:
			tts.say(("Venga va, esta es ya la última. Ahora alza la mano derecha lo más alto que puedas."))
			final = True
			print "final es true"
		else:
			tts.say(("Sigamos, solo un poco más, ahora alza la mano derecha lo más alto que puedas. Falta poco!"))
	elif nextposture == 5 and silla < 1:
		#falta el sitdown en el azul
		p.startBehavior("sitdown-271ebc/macarena")
		tts.say(("Ahora es momento de sentarse. Intenta sentarte igual que yo. A ver si lo consigues."))
		time.sleep(6)
		tts.say(("Lo estás clavando, estoy muy feliz."))
		time.sleep(1)
#Le pedimos al robot que nos haga una foto
def takephoto():
	global photo_taken
	session = qi.Session()
	session.connect("tcp://" + ip + ":" + str(port))
	video_service = session.service("ALVideoDevice")
	name = "python_client"
	cam_index = 0 #0 top 1 bottom
	resolution = 3 #8 es 40*30px 7 es 80*60px 0 es 160*120 1 es 320*240 2 es 640*480 3 es 1280*960
	colorSpace = 11 #9 es yuv442 y 11 es rgb
	fps = 10
	#videoClient = video_service.subscribeCamera("python_client", 3, 11, 5)
	videoClient = video_service.subscribeCamera(name,cam_index,resolution,colorSpace,fps)
	naoImage = video_service.getImageRemote(videoClient)
	video_service.unsubscribe(videoClient)
	imageWidth = naoImage[0]
	imageHeight = naoImage[1]
	array = naoImage[6]
	image_string = str(bytearray(array))
	# Create a PIL Image from our pixel array.
	im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)
	# Save the image.
	im.save("image.png", "PNG")
	processes = []
	copycmd = "cp image.png "+ruta+"/image_raw_"+str(nextposture)+".png"
	processes.append(subprocess.Popen(copycmd, shell = True))
	while not photo_taken:
		imagerecieved(archivo)




	#Esperamos recibir la foto
#Busca la foto recibida por NAO.
def imagerecieved(archivo):
    counter = 0
    global photo_taken
    try:
        fichero = open(archivo)
        fichero.close()
        photo_taken = True
        time.sleep(1)
    except:
        counter = counter+1
#Una vez recibida, tenemos que encontrar donde esta la cara
def facefinder(archivo):
	cara_x = 0
	cara_y = 0
	imageraw = cv2.imread(archivo)
	image = imutils.resize(imageraw,width = 600)
	faceCascade = cv2.CascadeClassifier(cascPath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(
	    gray,
	    scaleFactor=1.2,
	    minNeighbors=5,
	    minSize=(30, 30),
	    flags = cv2.CASCADE_SCALE_IMAGE
	)
	for (x, y, w, h) in faces:
		cara_x = x+w/2
		cara_y = y+h/2
  		face = image[y-30:y+h+30,x-30:x+w+30]

	if cara_x > 0:
		cv2.imwrite('face.png',face)
		processes = []
		copycmd = "cp face.png "+ruta+"/face_"+str(nextposture)+".png"
		processes.append(subprocess.Popen(copycmd, shell = True))

	print "Coordenadas cara:"
	print "x= ",cara_x
	print "y= ",cara_y
	print "-----------------------------"
	return cara_x,cara_y,image
#Ahora, toca encontrar el color que queramos
def color_recognition(lower,upper,cara_x,cara_y,image_tracted):
	x = 0
	y = 0
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
	hsv = cv2.cvtColor(image_tracted, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	kernel = np.ones((4,4),np.uint8)
	erode = cv2.erode(mask,kernel,iterations = 1)
	cnts  = cv2.findContours(erode.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	output = cv2.bitwise_and(hsv, hsv, mask = erode)
	if len(cnts) > 0:
		#buscamos su contorno
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		if radius > 10:
			print "x= ",x
			print "y= ",y
		else:
			x = 0
			y = 0
			print "x= ",x
			print "y= ",y
	# show the images
	print "-------------------------"
	return x, y
#Reconocemos qué postura ha hecho
def posturerecognition(face_x,face_y,yellow_x,yellow_y,green_x,green_y):
	postura = 0
	global cara
	if face_x == 0 or face_y == 0:
		postura = 0
		nocara1="No puedo verte la cara correctamente. Intenta mirarme a los ojos mientras haces el movimiento. Tú puedes."
		nocara2="No te veo bien. La próxima vez intenta mantener la mirada en mis ojos, sigue así!"
		nocara3="No he podido verte correctamente. Mantén tu cabeza mirando hacia mí, soy muy guapo."
		nocara4="No te veo con claridad. Recuerda que tienes que mirarme para que pueda reconocer tu cara"
		print "No se ha detectado cara"
		tts.say(choice([nocara1,nocara2,nocara3,nocara4]))
		cara = False
	else:
		if yellow_y == 0 and green_y == 0:
			print "No se ha detectado ninguna postura"
			postura = 5
		else:
			#sentado (más restrictiva)
			if (yellow_y > face_y and green_y > face_y and nextposture == 5):
				postura = 5
			#mano derecha(izq) arriba
			elif (yellow_y < face_y and green_y > face_y and yellow_y>0) or (yellow_y < face_y and green_y == 0 and yellow_y >0):
				postura = 4
			#Mano verde(izq)) arriba
			elif (yellow_y > face_y and green_y < face_y and green_y>0) or (green_y < face_y and yellow_y == 0 and green_y > 0):
				postura = 2
			#Dos brazos abajo
			elif yellow_y > face_y and green_y > face_y:
				postura = 3
			#Dos brazos arriba
			elif yellow_y < face_y and green_y < face_y:
				postura = 1
			else:
				print "No se ha detectado ninguna postura"
				postura = 6

	f = open(file_name,"a")
	distancia_dcha = math.sqrt(abs((face_x-yellow_x)**2 + (face_y-yellow_y)**2))
	distancia_izq = math.sqrt(abs((face_x-green_x)**2 + (face_y-green_y)**2))
	distancia_entre = math.sqrt(abs((green_x-yellow_x)**2 + (green_y-yellow_y)**2))
	towrite =  "____________________" +  "\n" + "Postura reconocida: "+ str(postura) +  "\n" + str(distancia_dcha) + "\n"+ str(distancia_izq) + "\n" + str(distancia_entre)
	f.write(towrite)
	f.close()

	return postura
#Escogemos siguiente postura según la lógica
def next_posture_on_game_logic(posture, nextposture):
	#Siguiente postura en la lógica del JUEGO
	#LO HA HECHO BIEN O NO.
	global fallos
	global final
	global pythoncmd

	f = open(file_name,"a")
	towrite =  "\n Postura que tenía que reconocer:" +str(nextposture) + "\n"
	f.write(towrite)
	f.close()


	if final:
		postureProxy = ALProxy("ALRobotPosture", ip, port)
		postureProxy.goToPosture("Stand",0.7)
		print "hola"
		pythoncmd = "nada"
		tts.say(("Ya hemos entrenado mucho por hoy, ¿descansamos un rato?"))
		postureProxy.goToPosture("Crouch",1.0)

	else:
		print "esto sigue y no se por qué"
		if posture == nextposture:
			fallos = 0
			motivacion1="Genial, lo estás haciendo perfecto."
			motivacion2="Maravilloso, sigue trabajando así, lo has clavado."
			motivacion3="Lo estás haciendo genial, sigue entrenando así."
			motivacion4="Perfecto, esa es la postura que yo quería."
			motivacion5="Qué bueno eres, sigamos entrenando así"
			tts.say(choice([motivacion1,motivacion2,motivacion3,motivacion4,motivacion5]))
			if posture == nextposture and posture == 5:
				postureProxy = ALProxy("ALRobotPosture", ip, port)
				print "correcto final"
				postureProxy.goToPosture("Stand",0.7)
				tts.say(("Ya hemos entrenado mucho por hoy, ¿descansamos un rato?"))
			#SI NO TERMINA EL JUEGO, ESCOGEMOS CUAL ES LA SIGUIENTE POSTURA
			if nextposture == 1:
				pythoncmd = "python ImitacionControl.py " + user + " " + str(sesion) +" 2" + " -s " +str(silla) + " -f " +str(fallos)
			elif nextposture == 0:
				pythoncmd = "python ImitacionControl.py " + user + " " + str(sesion) +" 1"+ " -s " +str(silla) +" -f " +str(fallos)
			elif nextposture == 2:
				pythoncmd = "python ImitacionControl.py " + user + " " + str(sesion) +" 3"+ " -s " +str(silla) +" -f " +str(fallos)
			elif nextposture == 3:
				pythoncmd = "python ImitacionControl.py " + user + " " + str(sesion) +" 4"+ " -s " +str(silla) +" -f " +str(fallos)
			elif nextposture == 4:
				pythoncmd = "python ImitacionControl.py " + user + " " + str(sesion) +" 5"+ " -s " +str(silla) +" -f " +str(fallos)

			subprocess.call(pythoncmd,shell=True)
		else:
			fallos += 1
			nextposture -= 1
			if fallos > 2:
				nextposture +=1
				tts.say(("No pasa nada, pasemos a la siguiente postura, seguro que la próxima la consigues."))
				fallos = 0
			else:
				if cara:
					fallo1="Has estado cerca. Vamos a volver a intentarlo con la misma postura."
					fallo2="Ha faltado poco. Volveremos a intentar la misma postura, tú puedes"
					fallo3="Hay que mejorarlo. Casi lo consigues, vamos a repetir la misma postura"
					fallo4="Muy cerca, pero no lo has clavado. Vamos a repetir la misma postura a ver si lo consigues."
					tts.say(choice([fallo1,fallo2,fallo3,fallo4]))

			if posture == nextposture and posture == 5:
				postureProxy = ALProxy("ALRobotPosture", ip, port)
				postureProxy.goToPosture("Stand",0.7)
				print "fallo final"
				tts.say(("Ya hemos entrenado mucho por hoy, ¿descansamos un rato?"))
				postureProxy.goToPosture("Crouch",1.0)
			#SI NO TERMINA EL JUEGO, ESCOGEMOS CUAL ES LA SIGUIENTE POSTURA
			if nextposture == 1:
				pythoncmd = "python ImitacionControl.py " + user + " " + str(sesion) +" 2" + " -s " + str(silla) +" -f " +str(fallos)
			elif nextposture == 0:
				pythoncmd = "python ImitacionControl.py " + user + " " + str(sesion) +" 1" + " -s " + str(silla) +" -f " +str(fallos)
			elif nextposture == 2:
				pythoncmd = "python ImitacionControl.py " + user + " " + str(sesion) +" 3" + " -s " + str(silla) +" -f " +str(fallos)
			elif nextposture == 3:
				pythoncmd = "python ImitacionControl.py " + user + " " + str(sesion) +" 4" + " -s " + str(silla) +" -f " +str(fallos)
			elif nextposture == 4:
				pythoncmd = "python ImitacionControl.py " + user + " " + str(sesion) +" 5" + " -s " + str(silla) +" -f " +str(fallos)

		subprocess.call(pythoncmd,shell=True)
#Iniciar la CNN de silvia pasandole como parámetro la imagen
def emotion_starter():
	processes = []
	copy = subprocess.Popen('cp face.png emote/imagen.png', shell = True)
	processes.append(copy)
	emotionchecker = subprocess.Popen('cd emote && ./init.sh', shell = True)
	processes.append(emotionchecker)

#____________________________________________________EL JUEGO EN Si______________________________
#Presentamos a NAO
if pres:
	presentacion()
print "CUANTOS FALLOS LLEVA"
print fallos
#Iniciamos el JUEGO
game_logic()

#Pedimos la foto al robot y esperamos recibirla
takephoto()

#Encontramos las coordenadas de la cara de la persona
cara_x, cara_y, image_tracted= facefinder(archivo)

#Iniciamos la CNN de Silvia
#emotion_starter()

#Calculamos donde esta el color amarillo y sus coordenadas
print "Coordenadas amarillo"
yellow_x, yellow_y = color_recognition(loweryellow,upperyellow,cara_x,cara_y,image_tracted)

#Calculamos donde esta el color verde y sus coordenadas
print "Coordenadas verdes"
green_x, green_y = color_recognition(lowergreen,uppergreen,cara_x,cara_y,image_tracted)

#Si no ha detectado verde con el primer tono, probamos con el segundo (detrás del guante)
if green_x == 0 and green_y == 0:
	green_x = 0
	green_x, green_y = color_recognition(lowerlightgreen,upperlightgreen,cara_x,cara_y,image_tracted)

#Calculamos la postura que tiene el jugador
posture = posturerecognition(cara_x,cara_y,yellow_x,yellow_y,green_x,green_y)
print "la postura reconocida:"
print posture

next_posture_on_game_logic(posture,nextposture)
print "ha salido de aquí y ahora que?"
