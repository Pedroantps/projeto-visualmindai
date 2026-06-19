import PyPDF2

def extract_text_from_pdf(filepath: str) -> str:
    """
    Extrai o texto de um arquivo PDF com tratamento de exceções.
    """
    extracted_text = ""
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        return extracted_text.strip()
    except Exception as e:
        raise Exception(f"Erro ao processar o PDF: {str(e)}")

def extract_text_from_txt(filepath: str) -> str:
    """
    Extrai o texto de um arquivo TXT comum.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        raise Exception(f"Erro ao processar o TXT: {str(e)}")