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

captura = cv2.VideoCapture(0, cv2.CAP_DSHOW) #acceso a la camara integrada del computador

with mp_face_detection.FaceDetection(min_detection_confidence=0.8) as face_detection:
    
    while(True):
        
        disponible, fotograma = captura.read()
        
        #Maquina de estados
        if(disponible == True and estado==0):
            estado = 1 #Empieza el programa
        elif(disponible == False and estado==0):
            estado = 3 #Error(camara no disponible o camara dañada)
        