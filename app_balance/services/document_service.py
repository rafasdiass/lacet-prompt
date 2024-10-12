# -*- coding: utf-8 -*-
"""
Serviço para processamento de documentos PDF e DOCX.
"""

from typing import List, Optional, Dict
import os
from PyPDF2 import PdfReader
from docx import Document


class DocumentService:
    """
    Serviço para ler e processar documentos PDF e DOCX.
    """

    def __init__(self, pdf_directory: Optional[str] = None, docx_directory: Optional[str] = None):
        """
        Inicializa o serviço de documentos com diretórios para PDFs e DOCXs.

        Args:
            pdf_directory (str, opcional): Diretório onde os PDFs estão localizados.
            docx_directory (str, opcional): Diretório onde os DOCXs estão localizados.
        """
        self.pdf_directory = pdf_directory
        self.docx_directory = docx_directory

    def read_pdf(self, file_path: str) -> str:
        """
        Lê e extrai o texto de um arquivo PDF.

        Args:
            file_path (str): Caminho para o arquivo PDF.

        Returns:
            str: Texto extraído do PDF.
        """
        if not os.path.exists(file_path) or not file_path.endswith('.pdf'):
            raise ValueError(f"Arquivo inválido ou inexistente: {file_path}")

        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise RuntimeError(f"Erro ao ler o PDF {file_path}: {str(e)}")

    def read_docx(self, file_path: str) -> str:
        """
        Lê e extrai o texto de um arquivo DOCX.

        Args:
            file_path (str): Caminho para o arquivo DOCX.

        Returns:
            str: Texto extraído do DOCX.
        """
        if not os.path.exists(file_path) or not file_path.endswith('.docx'):
            raise ValueError(f"Arquivo inválido ou inexistente: {file_path}")

        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            raise RuntimeError(f"Erro ao ler o DOCX {file_path}: {str(e)}")

    def process_all_pdfs(self) -> Dict[str, str]:
        """
        Processa todos os PDFs no diretório especificado e extrai o texto de cada um.

        Returns:
            dict: Dicionário com o nome do arquivo como chave e o texto extraído como valor.
        """
        if not self.pdf_directory:
            raise ValueError("Nenhum diretório de PDFs especificado.")
        if not os.path.exists(self.pdf_directory):
            raise FileNotFoundError(f"Diretório não encontrado: {self.pdf_directory}")

        pdf_texts = {}
        for filename in os.listdir(self.pdf_directory):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.pdf_directory, filename)
                pdf_texts[filename] = self.read_pdf(file_path)
        
        return pdf_texts

    def process_all_docxs(self) -> Dict[str, str]:
        """
        Processa todos os arquivos DOCX no diretório especificado e extrai o texto de cada um.

        Returns:
            dict: Dicionário com o nome do arquivo como chave e o texto extraído como valor.
        """
        if not self.docx_directory:
            raise ValueError("Nenhum diretório de DOCXs especificado.")
        if not os.path.exists(self.docx_directory):
            raise FileNotFoundError(f"Diretório não encontrado: {self.docx_directory}")

        docx_texts = {}
        for filename in os.listdir(self.docx_directory):
            if filename.endswith('.docx'):
                file_path = os.path.join(self.docx_directory, filename)
                docx_texts[filename] = self.read_docx(file_path)
        
        return docx_texts

    def process_all_documents(self) -> Dict[str, Dict[str, str]]:
        """
        Processa todos os PDFs e DOCXs nos diretórios especificados.

        Returns:
            dict: Dicionário com 'pdfs' e 'docxs' como chaves e os respectivos textos extraídos como valores.
        """
        pdfs = self.process_all_pdfs() if self.pdf_directory else {}
        docxs = self.process_all_docxs() if self.docx_directory else {}
        return {'pdfs': pdfs, 'docxs': docxs}
