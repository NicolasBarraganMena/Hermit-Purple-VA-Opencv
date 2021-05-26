# -*- coding: utf-8 -*-
"""
Created on Tue May 25 17:29:35 2021

@author: Nicolas Barragan
"""

import cv2
import mediapipe as mp
import pyautogui

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

#Guardara en que estado se encuentra actualmente el programa
# 0: Defecto, 1: Start, 2: Update, 3: Error
estado = 0

#captura
captura = cv2.VideoCapture(0, cv2.CAP_DSHOW) #acceso a la camara integrada del computador

with mp_face_detection.FaceDetection(min_detection_confidence=0.8) as face_detection:
    
    while(True):
        
        disponible, fotograma = captura.read()
        
        #Tamaño de la pantalla
        height, width, _ = fotograma.shape
        
        #Maquina de estados
        if(disponible == True and estado==0):
            estado = 1 #Empieza el programa
        elif(disponible == False and estado==0):
            estado = 3 #Error(camara no disponible o camara dañada)
        
        #Estados
        if(estado == 1): #Start
            print("Screen size: (" + str(width) + "," + str(height) + ")")
            estado = 2
        
        elif(estado == 2): #Update
            #print("Update")
            fotograma = cv2.flip(fotograma,1)
            fotograma_rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
            
            resultados = face_detection.process(fotograma_rgb)
            
            if resultados.detections is not None:
                for detection in resultados.detections:
                    #Nariz (NOSE_TIP)
                    xN = int(detection.location_data.relative_keypoints[2].x * width)
                    yN = int(detection.location_data.relative_keypoints[2].y * height)
                    #Dibujar un circulo en la punta de la nariz
                    cv2.circle(fotograma,(xN,yN),5,(255,255,0), -1)
            
            #Mostrar la captura
            cv2.imshow("Camara", fotograma)
            
            #Comandos de teclado
            if(cv2.waitKey(1) & 0xFF == ord('q')):
                #Liberar camara y destruir ventanas
                print("Finalizando")
                break
            
        elif(estado == 3): #Error
            print("Error, camara no disponible")
            break
        
#libera camara y destruye ventanas
captura.release()
cv2.destroyAllWindows()