import PyPDF2

def read_file(file):
    try:
        if file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        elif file.name.endswith(".txt"):
            return file.read().decode('utf-8')
        else:
            raise Exception("Unsupported file format only PDF and TXT files are supported")
    except Exception as e:
        raise Exception("Error reading the PDF file") from e
