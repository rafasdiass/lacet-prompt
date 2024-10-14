import os
import pandas as pd
import io
from typing import Optional, Dict
from PyPDF2 import PdfReader
from docx import Document
import logging

class FileProcessingService:
    def __init__(self, pdf_directory: Optional[str] = None, docx_directory: Optional[str] = None):
        self.pdf_directory = pdf_directory
        self.docx_directory = docx_directory

    def processar_arquivo(self, arquivo: bytes, tipo_arquivo: str) -> dict:
        """
        Processa arquivos Excel, PDF ou DOCX de acordo com o tipo especificado.
        Args:
            arquivo (bytes): O arquivo a ser processado.
            tipo_arquivo (str): O tipo do arquivo ('excel', 'pdf', 'docx').

        Returns:
            dict: Dados processados do arquivo.
        """
        if tipo_arquivo == 'excel':
            return self.processar_arquivo_excel(arquivo)
        elif tipo_arquivo == 'pdf':
            return {'texto': self.processar_arquivo_pdf(arquivo)}
        elif tipo_arquivo == 'docx':
            return {'texto': self.processar_arquivo_docx(arquivo)}
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {tipo_arquivo}")

    def processar_arquivo_excel(self, arquivo: bytes) -> dict:
        """
        Processa e extrai dados de um arquivo Excel.
        Args:
            arquivo (bytes): O arquivo Excel em bytes.

        Returns:
            dict: Dados processados com categorias e custos.
        """
        try:
            with io.BytesIO(arquivo) as excel_file:
                df = pd.read_excel(excel_file, sheet_name=None)

            data = {}
            for sheet_name, sheet_data in df.items():
                data[sheet_name] = sheet_data.to_dict(orient='records')

            return data

        except ValueError as ve:
            raise ValueError(f"Erro no formato do arquivo: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Erro ao processar arquivo Excel: {str(e)}")

    def processar_arquivo_pdf(self, arquivo: bytes) -> str:
        """
        Processa e extrai dados de um arquivo PDF.
        Args:
            arquivo (bytes): O arquivo PDF em bytes.

        Returns:
            str: Texto extraído do arquivo PDF.
        """
        try:
            texto_pdf = ""
            with io.BytesIO(arquivo) as pdf_file:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    texto_pdf += page.extract_text()

            return texto_pdf.strip()

        except Exception as e:
            raise RuntimeError(f"Erro ao processar arquivo PDF: {str(e)}")

    def processar_arquivo_docx(self, arquivo: bytes) -> str:
        """
        Processa e extrai dados de um arquivo DOCX.
        Args:
            arquivo (bytes): O arquivo DOCX em bytes.

        Returns:
            str: Texto extraído do arquivo DOCX.
        """
        try:
            texto_docx = ""
            with io.BytesIO(arquivo) as docx_file:
                documento = Document(docx_file)
                for paragrafo in documento.paragraphs:
                    texto_docx += paragrafo.text + "\n"

            return texto_docx.strip()

        except Exception as e:
            raise RuntimeError(f"Erro ao processar arquivo DOCX: {str(e)}")

    def processar_todos_documentos(self) -> Dict[str, Dict[str, str]]:
        """
        Processa todos os arquivos PDFs e DOCXs dos diretórios especificados.
        
        Returns:
            dict: Um dicionário contendo o texto de todos os PDFs e DOCXs.
        """
        pdfs = self.processar_todos_pdfs() if self.pdf_directory else {}
        docxs = self.processar_todos_docxs() if self.docx_directory else {}
        return {'pdfs': pdfs, 'docxs': docxs}

    def processar_todos_pdfs(self) -> Dict[str, str]:
        """
        Processa todos os arquivos PDF de um diretório.
        
        Returns:
            dict: Dicionário contendo os textos dos PDFs.
        """
        if not self.pdf_directory:
            raise ValueError("Nenhum diretório de PDFs especificado.")
        pdf_texts = {filename: self.processar_arquivo_pdf(os.path.join(self.pdf_directory, filename))
                     for filename in os.listdir(self.pdf_directory) if filename.endswith('.pdf')}
        return pdf_texts

    def processar_todos_docxs(self) -> Dict[str, str]:
        """
        Processa todos os arquivos DOCX de um diretório.
        
        Returns:
            dict: Dicionário contendo os textos dos DOCXs.
        """
        if not self.docx_directory:
            raise ValueError("Nenhum diretório de DOCXs especificado.")
        docx_texts = {filename: self.processar_arquivo_docx(os.path.join(self.docx_directory, filename))
                      for filename in os.listdir(self.docx_directory) if filename.endswith('.docx')}
        return docx_texts
