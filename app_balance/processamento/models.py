from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

# Classe Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'
    __table_args__ = {'extend_existing': True}
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

# Classe PromptModel
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
def criar_tabelas(engine):
    """Cria todas as tabelas no banco de dados."""
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso.")
