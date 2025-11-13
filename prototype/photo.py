import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import base64

def camera():
    #abre camera
    cam = cv2.VideoCapture(0) #0 opens default camera

    if not cam.isOpened():
        print('falha ao abrir camera')
        return None

    img = None
    while True:
        rt, frame = cam.read()
        if not rt:
            print('erro ao capturar frame')
            break

        cv2.imshow('Pressione \'c\' para captura o frame ou \'q\' para quitar' ,frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            img = None
            break
        if key == ord('c'):
            img = frame.copy()
            break   

    cam.release()
    cv2.destroyAllWindows()
    return img


def takePhoto():
    img = None
    while True:
        img = camera() #takes photo
        if img is not None:
            cv2.imshow("Pressione \'t\' para tirar outra foto ou \'f\' para prosseguir", img)
            key = cv2.waitKey(0) & 0xFF #waitKey(0) waits for user input
            if key == ord('f'):
                cv2.destroyAllWindows()
                return img, 'f' #ord() returns an int which != string
        else:
            return None, ''
        cv2.destroyAllWindows()


#loads photo from disk
def uploadPhoto():
    #inicialize tk
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    #opens explorer, with only jpg jpeg and png
    imgPath = askopenfilename(title='Selecione uma imagem', filetypes=[("Arquivos de image", "*.jpg *.jpeg *.png")])
    if imgPath:
        img = cv2.imread(imgPath)
        mode = 'f'
    else:
        img = None
        mode = ''
    root.destroy()
    return img, mode

def getPhoto():
    mode = input("\'t\'- Tirar foto\n\'u\'- Upload foto\n").lower()
    while True:   
        match mode:
            case 't':
                img, mode = takePhoto() #opens webcam and takes a pic

            case 'u':
                img, mode = uploadPhoto() #opens explorer to select a image file

            case _:
                mode = input("\'t\' - Tirar foto\n\'u\' - Upload foto\n").lower()

        #if there is no image operation was canceled
        if img is not None:
            break

    #converting image to base64
    _, buffer = cv2.imencode(".png", img)
    img_base64 = base64.b64encode(buffer).decode("utf-8")
    img_data = f"data:image/png;base64,{img_base64}"

    return img_data