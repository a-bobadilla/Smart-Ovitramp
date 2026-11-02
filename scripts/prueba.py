import cv2
import numpy as np

import os
archivos = os.listdir('dataset/')

from progress.bar import Bar

fechas = []
horas = []
cantidades = []

directorio = './dataset/'

progreso = Bar('Procesando :', max = len(archivos))

for archivo in archivos:
    #contador de larvas
    cLarvas = 0
    
    imagen = cv2.imread(directorio + archivo)
    grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    #se procede a realizar la umbralización con parámetros estáticos
    _,th = cv2.threshold(grises, 85, 255, cv2.THRESH_BINARY_INV)

    #se itera con operaciónes morfológicas sobre el resultado para eliminar el ruido
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN,kernel)

    #se utiliza el algortimo de detección por contornos para detección de objetos
    cnts,_ = cv2.findContours(opening,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #ciclo para recorrer los contornos y dibujar rectangulos
    for contorno in cnts:
        (x,y,w,h) = cv2.boundingRect(contorno)
        if w>11 and h>11:                                       #parametros estáticos para no dibujar contornos pequeños (suciedad)
            cv2.rectangle(imagen,(x,y),(x+w,y+h),(255,0,0),2)
            cLarvas=cLarvas+1
    
    cantidades.append(cLarvas)
    fechas.append(archivo[0:4]+'-'+archivo[5:6]+'-'+archivo[7:8])
    horas.append(archivo[9:10]+':'+archivo[11:12])

    progreso.next()

progreso.finish()