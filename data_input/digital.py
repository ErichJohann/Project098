from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
#    TesseractCliOcrOptions,
)
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import granite_picture_description
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

def doclingFormat(source):
    #ocr_options = TesseractCliOcrOptions(lang=["pt"])
    pipeline_options = PdfPipelineOptions(
        #do_ocr=True, force_full_page_ocr=True, ocr_options=ocr_options
    )
    pipeline_options.do_code_enrichment = True
    pipeline_options.do_formula_enrichment = True
    pipeline_options.generate_picture_images = True
    pipeline_options.images_scale = 2
    #pipeline_options.do_picture_classification = True
    pipeline_options.do_picture_description = True
    pipeline_options.picture_description_options = granite_picture_description

    doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
    result = doc_converter.convert(source)
    return result.document

if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    filePath = askopenfilename(
        title='Selecione o arquivo', 
        filetypes=[("Docs", "*.pdf")])

    if not filePath:
        print(f'Arquivo não foi selecionado')
        exit(1)

    doc = doclingFormat(filePath)

    print(doc.export_to_markdown())