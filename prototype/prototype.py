from photo import getPhoto
from scoutf import do_ocr
from tranquilizer import setPrompt
from slime import getAnswer
import json

if __name__ == '__main__':
    img_data = getPhoto()

    answer = do_ocr(img_data)

    teacher_Mode = setPrompt(answer)
    print("=============================================Prompt_Final====================================================")
    print(json.dumps(teacher_Mode, indent=2, ensure_ascii=False))

    response = getAnswer(teacher_Mode)

    print("\n\n=====================================================================================================")
    print(response)
    print("\n\n=====================================================================================================")