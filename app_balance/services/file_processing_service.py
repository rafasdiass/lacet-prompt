import pandas as pd
import io
from openpyxl import load_workbook
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app_balance.models import Recebimento
from app_balance.services.gpt_service import GPTService  # Refatorado para usar GPTService
from app_balance.services.prompt_service import PromptService  # Refatorado para usar PromptService

# Configuração do SQLite
DATABASE_URL = 'sqlite:///recebimentos.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class FileProcessingService:
    def __init__(self):
        self.gpt_service = GPTService()
        self.prompt_service = PromptService()

    def processar_arquivo_excel(self, arquivo: bytes) -> list:
        """Processa um arquivo Excel (.xlsx) e extrai recebimentos."""
        try:
            with io.BytesIO(arquivo) as excel_file:
                wb = load_workbook(excel_file)
                sheet = wb.active
                df = pd.DataFrame(sheet.values)

            recebimentos = []
            for _, row in df.iterrows():
                try:
                    recebimento = Recebimento(
                        data=datetime.strptime(row[0], '%Y-%m-%d').date(),
                        valor=float(row[1])
                    )
                    recebimentos.append(recebimento)
                except (ValueError, IndexError):
                    continue  # Ignora linhas com erros de conversão
            return recebimentos
        except Exception as e:
            raise RuntimeError(f"Erro ao processar arquivo Excel: {str(e)}")

    def salvar_recebimentos_no_db(self, recebimentos: list):
        """Salva uma lista de recebimentos no banco de dados SQLite."""
        try:
            session.add_all(recebimentos)
            session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Erro ao salvar os recebimentos no banco de dados: {str(e)}")

    def processar_arquivo(self, arquivo: bytes, tipo_arquivo: str) -> str:
        """Processa um arquivo com base no tipo fornecido e gera análise do GPT-4."""
        try:
            if tipo_arquivo == 'excel':
                recebimentos = self.processar_arquivo_excel(arquivo)
            else:
                raise ValueError(f"Tipo de arquivo não suportado: {tipo_arquivo}")

            # Salva recebimentos no banco de dados
            self.salvar_recebimentos_no_db(recebimentos)

            # Gera o prompt e envia para o GPT-4
            prompt = self.gpt_service.gerar_prompt_recebimentos(recebimentos)
            resposta_gpt = self.gpt_service.enviar_prompt(prompt)

            return resposta_gpt  # Retorna a resposta gerada pelo GPT-4 para exibição

        except Exception as e:
            raise RuntimeError(f"Erro ao processar arquivo: {str(e)}")
