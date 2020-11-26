import cv2
import imutils
import argparse
import numpy as np
from calibrador import *


image_video = None

lista_imagem_video_upper = []
lista_imagem_video_lower = []

lista_deslocamento_vertical = []


def trackingVideo(abrirVideo):

    camera = cv2.VideoCapture(abrirVideo)

    while True:

        # if None for igual a zero da um break do contrario faz a analise
        ###    circle_list = np.array(circulo).tolist()

        (grabbed, frame) = camera.read()

        if grabbed == False:
            break

        else:

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv, (46, 14, 34), (66, 34, 114))  # O QUE ESTAVA AQUI ANTES
            contorno_marcador = cv2.findContours(
                mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            centro = None

            # esse len aqui na verdade, vai pegar a quantidade de pixels que tem no contorno externo
            if len(contorno_marcador) > 0:

                i = max(contorno_marcador, key=cv2.contourArea)
                ((x, y), radiano) = cv2.minEnclosingCircle(i)
                M = cv2.moments(i)

                centro = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                cv2.circle(frame, (int(x), int(y)), int(radiano), 2)

                cv2.putText(frame, "LED", (int(x-radiano), int(y-radiano)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                #print("Vetor x(horizontal): ", int(x), "Vetor y(vertical): ", int(y))

                lista_deslocamento_vertical.append(int(y))

                # print(lista_deslocamento_vertical)

            cv2.imshow("Meu video", frame)  # printo o video
            cv2.imshow("Meu hsv", hsv)  # printo meu hsv
            cv2.imshow("Minha mask", mask)  # printo minha mask

            key = cv2.waitKey(1) & 0xFF

            # retorna um tempo para fechar
            # cv2.waitKey(0) --> n pode ter isto, pois congela a janela
