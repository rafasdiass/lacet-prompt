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

    # Strategy Pattern para definir se os dados devem ser persistidos ou não
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

    def save_gpt4_response(self, prompt_id: int, gpt4_response: str):
        """
        Salva a resposta gerada pela GPT-4 para um determinado prompt.
        """
        try:
            logging.info(f"Salvando resposta GPT-4 para o prompt {prompt_id}")
            gpt4_response_record = GPT4Response(
                prompt_id=prompt_id,
                resposta_gpt4=gpt4_response,
                data_resposta=datetime.now(),
            )
            self.session.add(gpt4_response_record)
            self.session.commit()
            logging.info(f"Resposta GPT-4 associada ao prompt {prompt_id} salva com sucesso.")
        except Exception as e:
            self.session.rollback()
            logging.error(f"Erro ao salvar resposta GPT-4: {str(e)}")
            raise RuntimeError(f"Erro ao salvar resposta GPT-4: {str(e)}")

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

    def get_latest_financial_data(self):
        """
        Busca e retorna o último registro financeiro salvo para o usuário atual.
        """
        try:
            logging.info(f"Buscando último registro financeiro para o usuário {self.usuario.nome}")
            recebimento = self.session.query(Recebimento).filter_by(usuario_id=self.usuario.id).order_by(Recebimento.data_recebimento.desc()).first()
            if recebimento:
                logging.info(f"Último registro encontrado: {recebimento}")
                return {
                    "total_custos": recebimento.total_custos,
                    "receita_projetada": recebimento.receita_projetada,
                    "categorias_custos": {recebimento.categoria: recebimento.valor},
                }
            else:
                logging.warning(f"Nenhum dado financeiro encontrado para o usuário {self.usuario.nome}")
                return None
        except Exception as e:
            logging.error(f"Erro ao buscar último dado financeiro: {str(e)}")
            return None
