from pypdf import PdfReader

def extract_text_from_pdf(file):
    """Extracts all readable text from uploaded PDF file."""
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        return f"PDF Error: {e}"
