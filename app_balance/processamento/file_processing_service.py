import pandas as pd
import io
from openpyxl import load_workbook
import datetime
from sqlalchemy.exc import SQLAlchemyError
import logging

class FileProcessingService:
    def __init__(self, session, usuario):
        self.session = session
        self.usuario = usuario

    def processar_arquivo_excel(self, arquivo: bytes) -> dict:
        try:
            with io.BytesIO(arquivo) as excel_file:
                wb = load_workbook(excel_file, data_only=True)
                sheet = wb.active
                df = pd.DataFrame(sheet.values)

            if df.shape[1] < 2:
                raise ValueError("O arquivo Excel deve conter ao menos duas colunas: 'Categoria' e 'Valor'.")

            categorias_custos = {}
            total_custos = 0.0

            for _, row in df.iterrows():
                try:
                    categoria = row[0]
                    valor = float(row[1])
                    categorias_custos[categoria] = categorias_custos.get(categoria, 0) + valor
                    total_custos += valor
                except (ValueError, IndexError) as e:
                    logging.error(f"Erro ao processar linha: {row} - {str(e)}")
                    continue

            receita_projetada = total_custos * 1.5
            self.salvar_dados_no_banco(categorias_custos, total_custos, receita_projetada)
            return {
                'categorias_custos': categorias_custos,
                'total_custos': total_custos,
                'receita_projetada': receita_projetada
            }

        except ValueError as ve:
            raise ValueError(f"Erro no formato do arquivo: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Erro ao processar arquivo Excel: {str(e)}")

    def salvar_dados_no_banco(self, categorias_custos: dict, total_custos: float, receita_projetada: float):
        try:
            from processamento.models import Recebimento
            for categoria, valor in categorias_custos.items():
                recebimento = Recebimento(
                    categoria=categoria,
                    valor=valor,
                    total_custos=total_custos,
                    receita_projetada=receita_projetada,
                    data_recebimento=datetime.datetime.now(),
                    usuario_id=self.usuario.id
                )
                self.session.add(recebimento)
            self.session.commit()
            logging.info(f"Dados inseridos no banco de dados com sucesso para o usuário {self.usuario.nome}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Erro ao inserir dados no banco de dados: {str(e)}")
