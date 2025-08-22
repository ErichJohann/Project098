import cv2

#abre camera
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print('falha ao abrir camera')
    exit(1)

imagem = None
while True:
    rt, frame = cam.read()
    if not rt:
        print('erro ao capturar frame')

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        imagem = frame.copy()
        break
    if key == ord('q'):
        break

    cv2.imshow('Pressione \'c\' para captura o frame ou \'q\' para sair' ,frame)

cam.release()
cv2.destroyAllWindows()