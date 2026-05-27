"""简历解析"""

import re
import PyPDF2
from docx import Document


def parse_resume(file_obj, file_type):
    if file_type == "pdf":
        return _parse_pdf(file_obj)
    elif file_type == "docx":
        return _parse_docx(file_obj)
    else:
        return None


def _parse_pdf(file_obj):
    reader = PyPDF2.PdfReader(file_obj)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return _clean(text)


def _parse_docx(file_obj):
    doc = Document(file_obj)
    text = "\n".join([p.text for p in doc.paragraphs])
    return _clean(text)


def _clean(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()