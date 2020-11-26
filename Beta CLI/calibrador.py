import cv2
import sys
import numpy as np

image_hsv = None
pixel = (20,60,80)

lista_upper = []
lista_lower = []

lista_centro_M = []
lista_centro_N = []

def pick_color(event,x,y,flags,param):

    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y,x]

        upper =  np.array([pixel[0] + 20, pixel[1] + 10, pixel[2] + 40])
        lower =  np.array([pixel[0] - 20, pixel[1] - 10, pixel[2] - 40])

        #print(lower, upper)
        lista_lower.append(lower)
        lista_upper.append(upper)


def start_Pick_color(image):
	global image_hsv, pixel

	cv2.namedWindow("hsv") # "hsv" são palavras reservadas para a mesma janela que eu coloquei o nome "hsv" segue ali em baixo
	cv2.setMouseCallback("hsv", pick_color) #inicia a função pick_color para a janela nomeada "hsv"

	image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	cv2.imshow("hsv", image_hsv)

	cv2.waitKey(0) # fazer alguma coisa para quando clicar seguir o curso do codigo // # aperte esc para segui adiante


def convertHSV(image):
	convert_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	return convert_hsv


def imageThreshould(image):
	thresh = cv2.inRange(convertHSV(image), lista_lower[0], lista_upper[0])
	return thresh


def contours(image):

	imgThresh = imageThreshould(image)

	circulo = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

	circulo1, circulo2 = circulo


	M = cv2.moments(circulo1)

	try:
		cM = int(M["m10"] / M["m00"])
	except ZeroDivisionError:
		print("Nao deu certo")
		cM = -1

	N = cv2.moments(circulo2)

	try:
		cN = int(M["m01"] / M["m00"])
	except ZeroDivisionError:
		print("Nao deu certo")
		cN = -1

	lista_centro_M.append(cM)
	lista_centro_N.append(cN)

	return draw(image, circulo1, circulo2, cM, cN)


def draw(image, circulo1, circulo2, cM, cN):

	cv2.drawContours(image, [circulo1], -1, (255, 0, 0), 2)
	cv2.drawContours(image, [circulo2], -1, (255, 0, 0), 2)
	
	
	#print(lista_centro_M)	# ele só esta pegando o valor daquele que eu seleciono?
	#print(lista_centro_N)
	
	
	#cv2.circle(image, (cM, cN), 7, (255, 255, 255), -1)
	#cv2.putText(image, "centro", (cM - 20, cN - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
	#cv2.putText(image, "X: {}, Y: {}".format(cM, cN),(cM -58, cN + 25), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1)

	cv2.imshow("Image", image)

	cv2.waitKey(0)


def meansure(lista_centro_M, lista_centro_N):
    distance = lista_centro_M[0] - lista_centro_N[0]

    #print("centro de M: ", lista_centro_M[0])
    #print("centro de N: ", lista_centro_N[0])
    #print(distance)

    return distance
