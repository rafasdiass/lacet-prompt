# -*- coding: utf-8 -*-
"""
Serviço para processamento de documentos PDF e DOCX.
"""

from typing import Optional, Dict
import os
from PyPDF2 import PdfReader
from docx import Document

class DocumentService:
    """
    Serviço para ler e processar documentos PDF e DOCX.
    """

    def __init__(self, pdf_directory: Optional[str] = None, docx_directory: Optional[str] = None):
        self.pdf_directory = pdf_directory
        self.docx_directory = docx_directory

    def read_pdf(self, file_path: str) -> str:
        if not os.path.exists(file_path) or not file_path.endswith('.pdf'):
            raise ValueError(f"Arquivo inválido ou inexistente: {file_path}")
        reader = PdfReader(file_path)
        text = "".join([page.extract_text() for page in reader.pages])
        return text

    def read_docx(self, file_path: str) -> str:
        if not os.path.exists(file_path) or not file_path.endswith('.docx'):
            raise ValueError(f"Arquivo inválido ou inexistente: {file_path}")
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def process_all_pdfs(self) -> Dict[str, str]:
        if not self.pdf_directory:
            raise ValueError("Nenhum diretório de PDFs especificado.")
        pdf_texts = {filename: self.read_pdf(os.path.join(self.pdf_directory, filename))
                     for filename in os.listdir(self.pdf_directory) if filename.endswith('.pdf')}
        return pdf_texts

    def process_all_docxs(self) -> Dict[str, str]:
        if not self.docx_directory:
            raise ValueError("Nenhum diretório de DOCXs especificado.")
        docx_texts = {filename: self.read_docx(os.path.join(self.docx_directory, filename))
                      for filename in os.listdir(self.docx_directory) if filename.endswith('.docx')}
        return docx_texts

    def process_all_documents(self) -> Dict[str, Dict[str, str]]:
        pdfs = self.process_all_pdfs() if self.pdf_directory else {}
        docxs = self.process_all_docxs() if self.docx_directory else {}
        return {'pdfs': pdfs, 'docxs': docxs}
