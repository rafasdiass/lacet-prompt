# -*- coding: utf-8 -*-
"""Módulo para processamento de arquivos."""

import pandas as pd
import PyPDF2
import io
from openpyxl import load_workbook

def processar_arquivo_excel(arquivo):
    """Processa um arquivo Excel (.xlsx) e retorna um DataFrame do pandas.

    Args:
        arquivo (bytes): O conteúdo do arquivo Excel.

    Returns:
        pd.DataFrame: O DataFrame resultante do arquivo Excel.
    """
    with io.BytesIO(arquivo) as excel_file:
        df = pd.read_excel(excel_file)
    return df

def processar_arquivo_pdf(arquivo):
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
