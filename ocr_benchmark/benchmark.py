import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def processData(path):
    #opens image on grayscale
    img = cv2.imread(r'imgs/invi.png', cv2.IMREAD_GRAYSCALE)
    binImg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 11) #thereshhold + binary
    denoisedImg = cv2.medianBlur(binImg, 3) #blur for noise removal
    cv2.imshow('a', denoisedImg)
    cv2.waitKey(0)
    return denoisedImg
    #return cv2.imread(r'imgs/internet.png')

def tes(img):
    confg = r'--oem 3 --psm 6'  # engine LSTM + modo "parágrafos"
    tesPredic = pytesseract.image_to_string(img, config=confg, lang='por')
    print(tesPredic)

def easy(img):
    return img

oi = processData('a')
tes(oi)