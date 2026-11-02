import cv2
import numpy as np

directorio = './dataset/'

#contador de larvas
cLarvas = 0

imagen = cv2.imread(directorio + '202210250828.jpg')
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)



#se procede a realizar la umbralización con parámetros estáticos
_,th = cv2.threshold(grises, 85, 255, cv2.THRESH_BINARY_INV)

#se itera con operaciónes morfológicas sobre el resultado para eliminar el ruido
kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(th, cv2.MORPH_OPEN,kernel)

#se utiliza el algortimo de detección por contornos para detección de objetos
cnts,_ = cv2.findContours(opening,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#Para ver los contornos descomente las líneas a continuación
#cv2.drawContours(imagen,cnts, -1,(255,0,0),2)


#ciclo para recorrer los contornos y dibujar rectangulos
for contorno in cnts:
    (x,y,w,h) = cv2.boundingRect(contorno)
    if w>11 and h>11:                                       #parametros estáticos para no dibujar contornos pequeños (suciedad)
        cv2.rectangle(imagen,(x,y),(x+w,y+h),(255,0,0),2)
        cLarvas=cLarvas+1


#Escribimos la cantidad de larvas detectadas
cv2.putText(imagen,'Cantidad de larvas : '+ str(cLarvas), (150, 40), 1, 2.5, (0, 255, 0), 3)
    
#se declara la ventana y nombre de la ventana a trabajar
cv2.namedWindow('SMART OVI',0)
cv2.resizeWindow('SMART OVI', 800, 600)


cv2.imshow('SMART OVI', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()