from sqlalchemy.orm import Session
from processamento.models import PromptModel, GPT4Response, Recebimento, Usuario
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

class DataPersistenceService:
    """
    Serviço para persistência de dados no banco de dados após o processamento.
    Implementa um padrão híbrido que decide a persistência com base no tipo de dado.
    """

    def __init__(self, session: Session, usuario: Usuario):
        if not session:
            raise ValueError("Sessão do banco de dados não foi fornecida")
        if not usuario:
            raise ValueError("Usuário não foi fornecido")
        self.session = session
        self.usuario = usuario
        logging.info(f"DataPersistenceService inicializado para o usuário: {usuario.nome}")

    def persist_data(self, data_type: str, **kwargs):
        """
        Define se os dados devem ser persistidos com base no tipo (prompt, financeiro, etc.).
        """
        if data_type == "financeiro":
            self.save_financial_analysis(**kwargs)
        elif data_type == "prompt":
            self.save_prompt_and_response(**kwargs)

    def save_prompt_and_response(self, prompt_text: str, response: str, source: str = "local"):
        """
        Salva um prompt e sua respectiva resposta gerada pela IA.
        """
        try:
            logging.info(f"Salvando prompt '{prompt_text}' e resposta '{response}' para o usuário {self.usuario.nome}")
            prompt = PromptModel(
                texto=prompt_text,
                resposta=response,
                origem_resposta=source,
                data_criacao=datetime.now(),
                usuario_id=self.usuario.id
            )
            self.session.add(prompt)
            self.session.commit()
            logging.info(f"Prompt e resposta salvos com sucesso para o usuário {self.usuario.nome}.")
        except Exception as e:
            self.session.rollback()
            logging.error(f"Erro ao salvar prompt e resposta: {str(e)}")
            raise RuntimeError(f"Erro ao salvar prompt e resposta: {str(e)}")

    def save_financial_analysis(self, categorias_custos: dict, total_custos: float, receita_projetada: float):
        """
        Salva os dados da análise financeira, incluindo as categorias de custo e receita projetada.
        """
        try:
            logging.info(f"Salvando análise financeira. Total de custos: {total_custos}, Receita projetada: {receita_projetada}")
            for categoria, valor in categorias_custos.items():
                recebimento = Recebimento(
                    categoria=categoria,
                    valor=valor,
                    total_custos=total_custos,
                    receita_projetada=receita_projetada,
                    data_recebimento=datetime.now(),
                    usuario_id=self.usuario.id,
                )
                self.session.add(recebimento)
            self.session.commit()
            logging.info(f"Análise financeira salva com sucesso.")
        except Exception as e:
            self.session.rollback()
            logging.error(f"Erro ao salvar análise financeira: {str(e)}")
            raise RuntimeError(f"Erro ao salvar análise financeira: {str(e)}")
