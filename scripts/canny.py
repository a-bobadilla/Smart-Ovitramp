import cv2

directorio = './dataset/'

imagen = cv2.imread(directorio + '202210242016.jpg')
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

_,th = cv2.threshold(grises, 75, 255, cv2.THRESH_BINARY_INV)

bordes = cv2.Canny(grises,255,70)

cv2.namedWindow('SMART OVI',0)
cv2.resizeWindow('SMART OVI', 800, 600)

#print("Numero de larvas detectados : ", str(len(cnts)))

cv2.imshow('SMART OVI',bordes)
cv2.waitKey(0)
cv2.destroyAllWindows()