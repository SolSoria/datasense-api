import os
import fitz
from docx2python import docx2python

def process_element(element):
    content = ""
    if isinstance(element, str):
        content += element + " "
    elif isinstance(element, list):
        for sub_element in element:
            content += process_element(sub_element)
    return content

def doc_extractor(file_name):
    content = ''
    # Convertir .docx a PDF
    document_name = file_name.split('.')[0]
    extension = file_name.split('.')[-1]
    
    # Construir la ruta completa al archivo
    file_path = os.path.join(file_name)
    doc = docx2python(file_path)

    # Extraer texto del PDF
    for paragraph in doc.body:
        for element in paragraph:
            content += process_element(element)

    return content