import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def camera():
    #abre camera
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print('falha ao abrir camera')
        exit(1)

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
        img = camera()
        if img is not None:
            cv2.imshow("Pressione \'t\' para tirar outra foto ou \'f\' para prosseguir", img)
            key = cv2.waitKey(0) & 0xFF
            if key == ord('f'):
                cv2.destroyAllWindows()
                return 'f', img
        else:
            return None, ''
        cv2.destroyAllWindows()


def uploadPhoto():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    imgPath = askopenfilename(title='Selecione uma imagem', filetypes=[("Arquivos de image", "*.jpg *.jpeg *.png")])
    if imgPath:
        img = cv2.imread(imgPath)
        mode = 'f'
    else:
        img = None
        mode = ''
    root.destroy()
    return img, mode


if __name__ == "__main__":
    mode = input("\'t\'- Tirar foto\n\'u\'- Upload foto\n").lower()
    while True:   
        match mode:
            case 't':
                img, mode = takePhoto()

            case 'u':
                img, mode = uploadPhoto()

            case _:
                mode = input("\'t\' - Tirar foto\n\'u\' - Upload foto\n").lower()
        if img is not None:
            print("imagem salva")
            break


    print("imagem enviada")