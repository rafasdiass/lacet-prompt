from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine  # Corrigido: Importando create_engine
from sqlalchemy.exc import SQLAlchemyError
import re
import bcrypt
from processamento.models import Usuario
import logging

# Configuração do banco de dados
DATABASE_URL = 'sqlite:///db.sqlite'
Session = sessionmaker(bind=create_engine(DATABASE_URL))  # Uso do create_engine
session = Session()

# Configurar logging
logging.basicConfig(level=logging.INFO)

class UserPreferencesService:
    """
    Serviço para gerenciar as preferências do usuário, como tipo de humor e outras configurações.
    """

    def __init__(self, session):
        """Construtor que inicializa a sessão do banco de dados."""
        self.session = session

    def criar_usuario_dinamico(self, nome: str, email: str, preferencias_tom: str, idioma_preferido: str, senha: str):
        """
        Cria um novo usuário pedindo os dados da interface gráfica.
        """
        try:
            # Valida o formato do email
            self.validar_email(email)

            # Verifica se o usuário já existe
            if self.session.query(Usuario).filter_by(nome=nome).first():
                raise ValueError(f"Usuário com nome '{nome}' já existe.")
            if self.session.query(Usuario).filter_by(email=email).first():
                raise ValueError(f"Usuário com email '{email}' já existe.")

            # Criptografar a senha
            hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

            # Criar e salvar o novo usuário no banco de dados
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                preferencias_tom=preferencias_tom,
                idioma_preferido=idioma_preferido,
                senha=hashed_password
            )
            self.session.add(novo_usuario)
            self.session.commit()
            logging.info(f"Usuário '{nome}' criado com sucesso.")
            return novo_usuario
        except SQLAlchemyError as e:
            self.session.rollback()
            logging.error(f"Erro ao criar o usuário: {str(e)}")
            raise RuntimeError(f"Erro ao criar o usuário: {str(e)}")
        except ValueError as e:
            logging.error(f"Erro de validação: {str(e)}")
            return None

    def carregar_usuario_existente(self, nome: str):
        """
        Carrega um usuário existente do banco de dados pelo nome.
        """
        try:
            usuario = self.session.query(Usuario).filter_by(nome=nome).first()
            if not usuario:
                logging.info(f"Usuário '{nome}' não encontrado.")
                return None
            logging.info(f"Usuário '{nome}' carregado com sucesso.")
            return usuario
        except SQLAlchemyError as e:
            self.session.rollback()
            logging.error(f"Erro ao carregar o usuário: {str(e)}")
            raise RuntimeError(f"Erro ao carregar o usuário: {str(e)}")

    def validar_email(self, email: str):
        """Valida se o email está no formato correto."""
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Email inválido.")

    def get_humor_atual(self, usuario: Usuario):
        """
        Retorna o humor atual do usuário, baseado nas suas preferências salvas.
        """
        try:
            humor_atual = usuario.preferencias_tom
            return humor_atual
        except Exception as e:
            logging.error(f"Erro ao obter o humor atual: {str(e)}")
            raise RuntimeError(f"Erro ao obter o humor atual: {str(e)}")
