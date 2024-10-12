# -*- coding: utf-8 -*-
"""Módulo para processamento de arquivos com integração ao banco de dados SQLite."""

import pandas as pd
import PyPDF2
import io
from openpyxl import load_workbook
from docx import Document
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuração do SQLite
DATABASE_URL = 'sqlite:///recebimentos.db'

# Configurar a engine e o session para o SQLite
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def processar_arquivo_excel(arquivo: bytes) -> list:
    """Processa um arquivo Excel (.xlsx) e retorna uma lista de recebimentos."""
    try:
        with io.BytesIO(arquivo) as excel_file:
            # Usar load_workbook do openpyxl para garantir a robustez no processamento
            wb = load_workbook(excel_file)
            sheet = wb.active
            df = pd.DataFrame(sheet.values)
            
        recebimentos = []
        for _, row in df.iterrows():
            try:
                recebimento = {
                    'data': datetime.strptime(row[0], '%Y-%m-%d').date(),
                    'valor': float(row[1])
                }
                recebimentos.append(recebimento)
            except (ValueError, IndexError):
                continue  # Pula linhas com erros de conversão
        return recebimentos
    except Exception as e:
        raise RuntimeError(f"Erro ao processar arquivo Excel: {str(e)}")

def processar_arquivo_pdf(arquivo: bytes) -> list:
    """Processa um arquivo PDF e retorna uma lista de recebimentos."""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(arquivo))
        recebimentos = []
        for page in reader.pages:
            texto = page.extract_text()
            linhas = texto.split('\n')
            for linha in linhas:
                try:
                    data_str, valor_str = linha.split(' ')
                    recebimento = {
                        'data': datetime.strptime(data_str, '%Y-%m-%d').date(),
                        'valor': float(valor_str)
                    }
                    recebimentos.append(recebimento)
                except (ValueError, IndexError):
                    continue  # Pula linhas com erros de conversão
        return recebimentos
    except Exception as e:
        raise RuntimeError(f"Erro ao processar arquivo PDF: {str(e)}")

def processar_arquivo_docx(arquivo: bytes) -> list:
    """Processa um arquivo DOCX e retorna uma lista de recebimentos."""
    try:
        documento = Document(io.BytesIO(arquivo))
        recebimentos = []
        for para in documento.paragraphs:
            try:
                data_str, valor_str = para.text.split(' ')
                recebimento = {
                    'data': datetime.strptime(data_str, '%Y-%m-%d').date(),
                    'valor': float(valor_str)
                }
                recebimentos.append(recebimento)
            except (ValueError, IndexError):
                continue  # Pula parágrafos com erros de conversão
        return recebimentos
    except Exception as e:
        raise RuntimeError(f"Erro ao processar arquivo DOCX: {str(e)}")

def salvar_recebimentos_no_db(recebimentos):
    """Salva uma lista de recebimentos no banco de dados SQLite."""
    try:
        for recebimento in recebimentos:
            session.execute(
                "INSERT INTO recebimentos (data, valor) VALUES (:data, :valor)",
                {'data': recebimento['data'], 'valor': recebimento['valor']}
            )
        session.commit()
    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Erro ao salvar os recebimentos no banco de dados: {str(e)}")

def processar_arquivo(arquivo: bytes, tipo_arquivo: str):
    """Processa um arquivo com base no tipo fornecido (Excel, PDF ou DOCX) e salva os dados no banco de dados."""
    try:
        if tipo_arquivo == 'excel':
            recebimentos = processar_arquivo_excel(arquivo)
        elif tipo_arquivo == 'pdf':
            recebimentos = processar_arquivo_pdf(arquivo)
        elif tipo_arquivo == 'docx':
            recebimentos = processar_arquivo_docx(arquivo)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {tipo_arquivo}")

        # Salvar os recebimentos no banco de dados
        salvar_recebimentos_no_db(recebimentos)
        
        return f"Processamento concluído para {tipo_arquivo}. {len(recebimentos)} recebimentos salvos no banco de dados."
    except Exception as e:
        raise RuntimeError(f"Erro ao processar arquivo: {str(e)}")
