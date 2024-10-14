import pandas as pd
import io
from openpyxl import load_workbook
from datetime import datetime
from app_balance.models import Recebimento
from sqlalchemy.orm import session
from create_db import Session

# Configuração do SQLite
session = Session()

class FileProcessingService:
    def processar_arquivo_excel(self, arquivo: bytes) -> dict:
        """
        Processa um arquivo Excel (.xlsx) e extrai dados financeiros.
        """
        try:
            with io.BytesIO(arquivo) as excel_file:
                wb = load_workbook(excel_file)
                sheet = wb.active
                df = pd.DataFrame(sheet.values)

            categorias_custos = {}
            total_custos = 0.0

            for _, row in df.iterrows():
                try:
                    categoria = row[0]
                    valor = float(row[1])
                    categorias_custos[categoria] = categorias_custos.get(categoria, 0) + valor
                    total_custos += valor
                except (ValueError, IndexError):
                    continue  # Ignora linhas com erros de conversão

            receita_projetada = total_custos * 1.5  # Simulação de receita projetada com base nos custos

            return {
                'categorias_custos': categorias_custos,
                'total_custos': total_custos,
                'receita_projetada': receita_projetada
            }
        except Exception as e:
            raise RuntimeError(f"Erro ao processar arquivo Excel: {str(e)}")
