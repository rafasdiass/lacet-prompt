# data_persistence_service.py
from sqlalchemy.orm import Session
from processamento.models import Prompt, GPT4Response, Recebimento, Usuario
from datetime import datetime


class DataPersistenceService:
    """
    Serviço que atua como a última etapa no processamento, responsável por armazenar as respostas
    no banco de dados após a análise e processamento.
    """

    def __init__(self, session: Session, usuario: Usuario):
        """
        Inicializa o serviço de persistência de dados com uma sessão de banco de dados e o usuário associado.

        Args:
            session (Session): Sessão do banco de dados.
            usuario (Usuario): Usuário ao qual os dados estão relacionados.
        """
        self.session = session
        self.usuario = usuario

    def save_prompt_and_response(
        self, prompt_text: str, response: str, source: str = "local"
    ):
        """
        Salva o prompt e sua resposta no banco de dados.

        Args:
            prompt_text (str): Texto do prompt feito pelo usuário.
            response (str): Resposta gerada (seja local ou GPT-4).
            source (str): Origem da resposta (ex: 'local' ou 'GPT-4').
        """
        try:
            prompt = Prompt(
                texto=prompt_text,
                resposta=response,
                origem_resposta=source,
                data_criacao=datetime.now(),
                usuario_id=self.usuario.id,
            )
            self.session.add(prompt)
            self.session.commit()
            print(
                f"Prompt e resposta salvos com sucesso para o usuário {self.usuario.nome}."
            )
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(
                f"Erro ao salvar prompt e resposta no banco de dados: {str(e)}"
            )

    def save_gpt4_response(self, prompt_id: int, gpt4_response: str):
        """
        Salva uma resposta gerada pelo GPT-4 associada a um prompt no banco de dados.

        Args:
            prompt_id (int): ID do prompt associado.
            gpt4_response (str): Resposta gerada pelo GPT-4.
        """
        try:
            gpt4_response_record = GPT4Response(
                prompt_id=prompt_id,
                resposta_gpt4=gpt4_response,
                data_resposta=datetime.now(),
            )
            self.session.add(gpt4_response_record)
            self.session.commit()
            print(
                f"Resposta do GPT-4 associada ao prompt {prompt_id} salva com sucesso."
            )
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(
                f"Erro ao salvar resposta do GPT-4 no banco de dados: {str(e)}"
            )

    def save_financial_analysis(
        self, categorias_custos: dict, total_custos: float, receita_projetada: float
    ):
        """
        Salva uma análise financeira no banco de dados após o processamento.

        Args:
            categorias_custos (dict): Dicionário contendo as categorias e os custos associados.
            total_custos (float): Total de custos.
            receita_projetada (float): Receita projetada.
        """
        try:
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
            print(
                f"Análise financeira salva com sucesso para o usuário {self.usuario.nome}."
            )
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(
                f"Erro ao salvar análise financeira no banco de dados: {str(e)}"
            )

    def get_user_prompts(self):
        """
        Retorna uma lista de todos os prompts associados ao usuário atual.

        Returns:
            list: Lista de prompts associados ao usuário.
        """
        return self.session.query(Prompt).filter_by(usuario_id=self.usuario.id).all()

    def get_user_financial_data(self):
        """
        Retorna todos os registros financeiros associados ao usuário atual.

        Returns:
            list: Lista de registros financeiros associados ao usuário.
        """
        return (
            self.session.query(Recebimento).filter_by(usuario_id=self.usuario.id).all()
        )

    def get_latest_financial_data(self):
        """
        Busca o último registro financeiro associado ao usuário.
        """
        try:
            recebimento = (
                self.session.query(Recebimento)
                .filter_by(usuario_id=self.usuario.id)
                .order_by(Recebimento.data_recebimento.desc())
                .first()
            )

            if recebimento:
                return {
                    "total_custos": recebimento.total_custos,
                    "receita_projetada": recebimento.receita_projetada,
                    "categorias_custos": {recebimento.categoria: recebimento.valor},
                }
            else:
                return None
        except Exception as e:
            print(f"Erro ao buscar dados financeiros: {str(e)}")
            return None
