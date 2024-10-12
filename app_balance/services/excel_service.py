# -*- coding: utf-8 -*-
"""Serviço para processar arquivos Excel."""

import pandas as pd

def process_excel_file(file):
    """Lê um arquivo Excel e retorna os dados em formato JSON.

    Args:
        file (FileStorage): O arquivo Excel enviado.

    Returns:
        list: Lista de dicionários representando os dados das planilhas.
    """
    # Ler a planilha Excel
    excel_data = pd.read_excel(file, sheet_name=None)

    # Converter para JSON
    data = {}
    for sheet_name, sheet_data in excel_data.items():
        data[sheet_name] = sheet_data.to_dict(orient='records')
    
    return data
