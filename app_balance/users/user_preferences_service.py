from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app_balance.processamento.models import Usuario  # Certifique-se de que o caminho está correto
from sqlalchemy.exc import SQLAlchemyError
import re

# Configuração do banco de dados
DATABASE_URL = 'sqlite:///db.sqlite'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class UserPreferencesService:
    """
    Serviço para gerenciar as preferências do usuário, como tipo de humor e outras configurações.
    """

    def criar_usuario_dinamico(self, nome: str, email: str, preferencias_tom: str, idioma_preferido: str):
        """
        Cria um novo usuário pedindo os dados da interface gráfica.
        """
        try:
            # Valida o formato do email
            self.validar_email(email)

            # Verifica se o usuário já existe
            if session.query(Usuario).filter_by(nome=nome).first():
                raise ValueError(f"Usuário com nome '{nome}' já existe.")
            if session.query(Usuario).filter_by(email=email).first():
                raise ValueError(f"Usuário com email '{email}' já existe.")

            # Criar e salvar o novo usuário no banco de dados
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                preferencias_tom=preferencias_tom,
                idioma_preferido=idioma_preferido
            )
            session.add(novo_usuario)
            session.commit()
            print(f"Usuário '{nome}' criado com sucesso.")
            return novo_usuario
        except SQLAlchemyError as e:
            session.rollback()
            raise RuntimeError(f"Erro ao criar o usuário: {str(e)}")
        except ValueError as e:
            print(f"Erro de validação: {str(e)}")
            return None

    def carregar_usuario_existente(self, nome: str):
        """
        Carrega um usuário existente do banco de dados pelo nome.
        """
        try:
            usuario = session.query(Usuario).filter_by(nome=nome).first()
            if not usuario:
                print(f"Usuário '{nome}' não encontrado.")
                return None
            print(f"Usuário '{nome}' carregado com sucesso.")
            return usuario
        except SQLAlchemyError as e:
            session.rollback()
            raise RuntimeError(f"Erro ao carregar o usuário: {str(e)}")

    def validar_email(self, email: str):
        """Valida se o email está no formato correto."""
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Email inválido.")

    def get_humor_atual(self, usuario: Usuario):
        """
        Retorna o humor atual do usuário, baseado nas suas preferências salvas.
        Args:
            usuario (Usuario): O usuário carregado do banco de dados.
        """
        try:
            humor_atual = usuario.preferencias_tom
            return humor_atual
        except Exception as e:
            raise RuntimeError(f"Erro ao obter o humor atual: {str(e)}")
