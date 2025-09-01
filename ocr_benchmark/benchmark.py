import pytesseract
import easyocr
from paddleocr import PaddleOCR
import cv2

def processData(path):
    #opens image on grayscale
    img = cv2.imread(r'imgs/chaff.png', cv2.IMREAD_GRAYSCALE)
    #weighted mean threshold + binary
    binImg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 11)
    denoisedImg = cv2.medianBlur(binImg, 3) #blur for noise removal
    #cv2.imshow('a', denoisedImg) #show image after processing
    #cv2.waitKey(0)
    #return denoisedImg
    return cv2.imread(r'imgs/traffic.png')


#may have more accuracy preprocessing data effectively
def tes(img):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" #default tesseract path
    confg = r'--oem 3 --psm 6'  # engine LSTM + modo "parágrafos"
    tesPredict = pytesseract.image_to_string(img, config=confg, lang='por')
    print(tesPredict)


def easy(img):
    reader = easyocr.Reader(['pt'])
    #default=greety--> fast less accurate | beamsearch--> more accurate
    predict = reader.readtext(img, detail=0, paragraph=True, decoder='beamsearch')

    for txt in predict:
        print(txt + ' ')


def paddle(img):
    #text image preprocessing + text detection + textline orientation classification + text recognition
    ocr = PaddleOCR(use_doc_orientation_classify=True, use_doc_unwarping=True, lang='pt')
    dat = ocr.predict(img)

    predict = dat[0]
    for line in predict['rec_texts']:
        print(line)


oi = processData('a')
paddle(oi)