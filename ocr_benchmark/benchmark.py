import pytesseract
import cv2

def processData(path):
    #opens image on grayscale
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    binImg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 11) #thereshhold + binary
    denoisedImg = cv2.medianBlur(binImg, 3) #blur for noise removal

    return denoisedImg