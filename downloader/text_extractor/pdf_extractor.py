import fitz  # PyMuPDF

def pdf_extractor(file_path):
    text = ""
    with fitz.open(file_path) as pdf_file:
        for page_num in range(pdf_file.page_count):
            page = pdf_file.load_page(page_num)
            text += page.get_text()
    return text