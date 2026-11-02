import cv2
import numpy as np

directorio = './dataset/'

hsv_min = np.array([0,36,43], np.uint8)
hsv_max = np.array([176,199,104], np.uint8)

def test1():
    imagen = cv2.imread(directorio + '202210242016.jpg')
    imagen_rgb = cv2.cvtColor(imagen,cv2.COLOR_RGB2BGR)

    hsv = cv2.cvtColor(imagen,cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, hsv_min, hsv_max)

    #Buscamos contornos con las mascaras
    _,contornos = cv2.findContours(mascara, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imagen_rgb, contornos, -1,(255,0,0),2)

    cv2.namedWindow('SMART OVI',0)
    cv2.resizeWindow('SMART OVI', 800, 600)
    
    cv2.imshow('SMART OVI',imagen_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    test1() 
