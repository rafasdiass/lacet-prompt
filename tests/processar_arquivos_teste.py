# -*- coding: utf-8 -*-
"""Teste para o processamento de arquivos."""

import sys
import os

# Adiciona o diretório raiz do projeto ao caminho para permitir a importação de módulos.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app_balance')))

from file_processing import processar_arquivo

# Caminho para a pasta de exemplos dentro de app_balance
pasta_exemplos = os.path.join(os.path.dirname(__file__), '..', 'app_balance', 'exemplo')

# Exemplo de processamento de um arquivo Excel
with open(os.path.join(pasta_exemplos, 'exemplo.xlsx'), 'rb') as f:
    conteudo_excel = f.read()
    df_excel = processar_arquivo(conteudo_excel, 'excel')
    print("Conteúdo do Excel:")
    print(df_excel)

# Exemplo de processamento de um arquivo PDF
with open(os.path.join(pasta_exemplos, 'exemplo.pdf'), 'rb') as f:
    conteudo_pdf = f.read()
    texto_pdf = processar_arquivo(conteudo_pdf, 'pdf')
    print("Conteúdo do PDF:")
    print(texto_pdf)

# Exemplo de processamento de um arquivo DOCX
with open(os.path.join(pasta_exemplos, 'exemplo.docx'), 'rb') as f:
    conteudo_docx = f.read()
    texto_docx = processar_arquivo(conteudo_docx, 'docx')
    print("Conteúdo do DOCX:")
    print(texto_docx)
