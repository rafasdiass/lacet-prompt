# -*- coding: utf-8 -*-
"""Módulo para processamento de arquivos."""

import pandas as pd
import PyPDF2
import io
from openpyxl import load_workbook
from docx import Document

def processar_arquivo_excel(arquivo: bytes) -> pd.DataFrame:
    """Processa um arquivo Excel (.xlsx) e retorna um DataFrame do pandas.

    Args:
        arquivo (bytes): O conteúdo do arquivo Excel.

    Returns:
        pd.DataFrame: O DataFrame resultante do arquivo Excel.
    """
    with io.BytesIO(arquivo) as excel_file:
        df = pd.read_excel(excel_file)
    return df

def processar_arquivo_pdf(arquivo: bytes) -> str:
    """Processa um arquivo PDF e retorna o texto extraído.

    Args:
        arquivo (bytes): O conteúdo do arquivo PDF.

    Returns:
        str: O texto extraído do PDF.
    """
    reader = PyPDF2.PdfReader(io.BytesIO(arquivo))
    texto_extraido = ""
    for page in reader.pages:
        texto_extraido += page.extract_text() + "\n"
    return texto_extraido

def processar_arquivo_docx(arquivo: bytes) -> str:
    """Processa um arquivo DOCX e retorna o texto extraído.

    Args:
        arquivo (bytes): O conteúdo do arquivo DOCX.

    Returns:
        str: O texto extraído do DOCX.
    """
    documento = Document(io.BytesIO(arquivo))
    texto_extraido = "\n".join([paragrafo.text for paragrafo in documento.paragraphs])
    return texto_extraido

def processar_arquivo(arquivo: bytes, tipo_arquivo: str):
    """Processa um arquivo com base no tipo fornecido (Excel, PDF ou DOCX).

    Args:
        arquivo (bytes): O conteúdo do arquivo.
        tipo_arquivo (str): O tipo do arquivo, que pode ser 'excel', 'pdf' ou 'docx'.

    Returns:
        Dependendo do tipo de arquivo:
        - pd.DataFrame: Para arquivos Excel.
        - str: Para arquivos PDF e DOCX.
    """
    if tipo_arquivo == 'excel':
        return processar_arquivo_excel(arquivo)
    elif tipo_arquivo == 'pdf':
        return processar_arquivo_pdf(arquivo)
    elif tipo_arquivo == 'docx':
        return processar_arquivo_docx(arquivo)
    else:
        raise ValueError(f"Tipo de arquivo não suportado: {tipo_arquivo}")
