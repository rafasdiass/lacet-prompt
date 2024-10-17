from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.exc import SQLAlchemyError
import re
import bcrypt
import datetime
from processamento.models import PromptModel, GPT4Response, Recebimento, Usuario
from processamento.database_setup import Base

# Configuração do banco de dados
DATABASE_URL = 'sqlite:///db.sqlite'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

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
            print(f"Usuário '{nome}' criado com sucesso.")
            return novo_usuario
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Erro ao criar o usuário: {str(e)}")
        except ValueError as e:
            print(f"Erro de validação: {str(e)}")
            return None

    def carregar_usuario_existente(self, nome: str):
        """
        Carrega um usuário existente do banco de dados pelo nome.
        """
        try:
            usuario = self.session.query(Usuario).filter_by(nome=nome).first()
            if not usuario:
                print(f"Usuário '{nome}' não encontrado.")
                return None
            print(f"Usuário '{nome}' carregado com sucesso.")
            return usuario
        except SQLAlchemyError as e:
            self.session.rollback()
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
            raise RuntimeError(f"Erro ao obter o humor atual: {str(e)}")


class DataPersistenceService:
    """
    Serviço para persistência de dados no banco de dados após o processamento.
    """

    def __init__(self, session, usuario):
        if not session:
            raise ValueError("Sessão do banco de dados não foi fornecida")
        if not usuario:
            raise ValueError("Usuário não foi fornecido")
        self.session = session
        self.usuario = usuario

    def save_prompt_and_response(self, prompt_text: str, response: str, source: str = "local"):
        """
        Salva o prompt e a resposta gerada para o usuário no banco de dados.
        """
        try:
            prompt = PromptModel(  # Usando PromptModel
                texto=prompt_text,
                resposta=response,
                origem_resposta=source,
                data_criacao=datetime.datetime.now(),
                usuario_id=self.usuario.id
            )
            self.session.add(prompt)
            self.session.commit()
            print(f"Prompt e resposta salvos com sucesso para o usuário {self.usuario.nome}.")
        except Exception as e:
            self.session.rollback()
            print(f"Erro ao salvar prompt e resposta: {str(e)}")
            raise RuntimeError(f"Erro ao salvar prompt e resposta: {str(e)}")

    def save_gpt4_response(self, prompt_id: int, gpt4_response: str):
        """
        Salva a resposta da GPT-4 associada a um prompt.
        """
        try:
            gpt4_response_record = GPT4Response(
                prompt_id=prompt_id,
                resposta_gpt4=gpt4_response,
                data_resposta=datetime.datetime.now(),
            )
            self.session.add(gpt4_response_record)
            self.session.commit()
            print(f"Resposta GPT-4 associada ao prompt {prompt_id} salva com sucesso.")
        except Exception as e:
            self.session.rollback()
            print(f"Erro ao salvar resposta GPT-4: {str(e)}")
            raise RuntimeError(f"Erro ao salvar resposta GPT-4: {str(e)}")

    def save_financial_analysis(self, categorias_custos: dict, total_custos: float, receita_projetada: float):
        """
        Salva a análise financeira, incluindo as categorias de custo e receita projetada.
        """
        try:
            for categoria, valor in categorias_custos.items():
                recebimento = Recebimento(
                    categoria=categoria,
                    valor=valor,
                    total_custos=total_custos,
                    receita_projetada=receita_projetada,
                    data_recebimento=datetime.datetime.now(),
                    usuario_id=self.usuario.id,
                )
                self.session.add(recebimento)
            self.session.commit()
            print("Análise financeira salva com sucesso.")
        except Exception as e:
            self.session.rollback()
            print(f"Erro ao salvar análise financeira: {str(e)}")
            raise RuntimeError(f"Erro ao salvar análise financeira: {str(e)}")


# Classe Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela se já existir
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(128), nullable=False)
    preferencias_tom = Column(String(50), nullable=False)
    idioma_preferido = Column(String(10), nullable=False)

    # Relacionamento com a tabela PromptModel
    prompts = relationship('PromptModel', back_populates='usuario')


# Classe Recebimento
class Recebimento(Base):
    __tablename__ = 'recebimentos'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    categoria = Column(String(50), nullable=False)
    valor = Column(Float, nullable=False)
    total_custos = Column(Float, nullable=False)
    receita_projetada = Column(Float, nullable=False)
    data_recebimento = Column(DateTime, default=datetime.datetime.now)

    # Relacionamento com a tabela Usuario
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))


# Classe PromptModel (foi renomeada)
class PromptModel(Base):
    __tablename__ = 'prompts'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    texto = Column(Text, nullable=False)
    resposta = Column(Text, nullable=False)
    categoria = Column(String(50), nullable=False, default="geral")
    origem_resposta = Column(String(50), nullable=False, default="local")
    data_criacao = Column(DateTime, default=datetime.datetime.now)

    # Relacionamento com a tabela Usuario
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship('Usuario', back_populates='prompts')

    # Relacionamento com as respostas da GPT-4
    gpt4_responses = relationship('GPT4Response', back_populates='prompt')

    # Relacionamento com as análises
    analises = relationship('Analise', back_populates='prompt')


# Classe GPT4Response
class GPT4Response(Base):
    __tablename__ = 'gpt4_responses'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    prompt_id = Column(Integer, ForeignKey('prompts.id'))
    resposta_gpt4 = Column(Text, nullable=False)
    data_resposta = Column(DateTime, default=datetime.datetime.now)

    # Relacionamento com a tabela PromptModel
    prompt = relationship('PromptModel', back_populates='gpt4_responses')


# Classe Analise (para armazenar análises feitas sobre os prompts)
class Analise(Base):
    __tablename__ = 'analises'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    tipo_analise = Column(String(50), nullable=False)  # Ex: 'financeira', 'geral', 'humor'
    resultado = Column(Text, nullable=False)  # Armazena o relatório ou resultado da análise
    data_analise = Column(DateTime, default=datetime.datetime.now)

    # Relacionamento com a tabela PromptModel
    prompt_id = Column(Integer, ForeignKey('prompts.id'))
    prompt = relationship('PromptModel', back_populates='analises')


# Função para criar todas as tabelas no banco de dados
def criar_tabelas():
    """Cria todas as tabelas no banco de dados."""
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso.")
