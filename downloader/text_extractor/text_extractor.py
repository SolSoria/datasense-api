from .csv_extractor import csv_extractor
from .doc_extractor import doc_extractor
from .pdf_extractor import pdf_extractor
from .xls_extractor import xls_extractor
from .ppt_extractor import ppt_extractor

def text_extractor(file_path):
    # Extracts text from a file
    extension = file_path.split('.')[-1]
    if extension == 'csv':
        return csv_extractor(file_path)
    elif extension == 'pdf':
        return pdf_extractor(file_path)
    elif extension == 'docx':
        return doc_extractor(file_path)
    elif extension == 'xlsx':
        return xls_extractor(file_path)
    elif extension == 'pptx':
        return ppt_extractor(file_path)
    else:
        raise ValueError(f'Unsupported file format: {extension}')