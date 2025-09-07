from docling.document_converter import DocumentConverter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

def doclingFormat(source):
    converter = DocumentConverter()
    doc = converter.convert(source).document
    return doc

if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    filePath = askopenfilename(
        title='Selecione o arquivo', 
        filetypes=[("Docs", "*.pdf *.docx *.pptx")])

    if not filePath:
        print(f'Arquivo não foi selecionado')
        exit(1)

    doc = doclingFormat(filePath)

    print(doc.export_to_markdown())