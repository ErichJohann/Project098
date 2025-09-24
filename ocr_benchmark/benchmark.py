import pytesseract
import easyocr
from paddleocr import PaddleOCR
#from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
import cv2
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pix2tex.cli import LatexOCR
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" #default tesseract path
confg = r'--oem 3 --psm 6'  # engine LSTM + modo "parágrafos"

'''os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
device = 'cuda' if torch.cuda.is_available() else 'cpu'
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-handwritten")
model.to(device)
model.eval()'''


def processData(path):
    '''opens image on grayscale
    img = cv2.imread(r'imgs/rocket.png', cv2.IMREAD_GRAYSCALE)
    weighted mean threshold + binary
    binImg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 11)
    denoisedImg = cv2.medianBlur(binImg, 3) #blur for noise removal
    cv2.imshow('a', denoisedImg) #show image after processing
    cv2.waitKey(0)
    return denoisedImg'''
    return cv2.imread(r'.png')


#may have more accuracy preprocessing data effectively
def tes(img):
    tesPredict = pytesseract.image_to_string(img, config=confg, lang='por')
    print(tesPredict)


def easy(img):
    reader = easyocr.Reader(['pt'])
    #default=greety--> fast less accurate | beamsearch--> more accurate
    predict = reader.readtext(img, detail=0, decoder='beamsearch', paragraph=True)

    for txt in predict:
        print(txt + ' ')


def paddle(img):
    #text image preprocessing + text detection + textline orientation classification + text recognition
    ocr = PaddleOCR(use_doc_orientation_classify=True, use_doc_unwarping=True, lang='pt')
    dat = ocr.predict(img)

    predict = dat[0]
    for line in predict['rec_texts']:
        print(line)
        

'''def tr(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #h, w, _ = img.shape
    #scale = 384 / max(h, w)
    #img = cv2.resize(img, (int(w*scale), int(h*scale)))
    print(f"running on: {device}")


    pixel_values = processor(images=img, return_tensors='pt').pixel_values.to(device)

    with torch.no_grad():
        generated_ids = model.generate(
            pixel_values,
            max_new_tokens=1023,
            num_beams=5,
            early_stopping=True
        )
        
    #generated_ids = model.generate(pixel_values, max_new_tokens=1000)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(f"texto identificado: {text}")'''


def latOcr(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    model = LatexOCR()
    result = model(img)
    print(result)


def getImg():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    imgPath = askopenfilename(title='Selecione uma imagem', filetypes=[("Arquivos de image", "*.jpg *.jpeg *.png")])
    return imgPath

imPath = getImg()
oi = cv2.imread(imPath)
#print("\n\n=======Tesseract=======\n")
#tes(oi)

#print("\n\n=======EasyOCR=======\n")
#easy(oi)

#print("\n\n=======PaddleOCR=======\n")
#paddle(oi)

#print("\n\n=======TrOCR=======\n")
#tr(oi)

print("\n\n=======LatexOCR=======\n")
latOcr(oi)