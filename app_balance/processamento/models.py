from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from app_balance.processamento.database_setup import Base  # Ajustado o caminho da importação
import datetime

# Classe Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela se já existir
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)  # Limite de 50 caracteres
    email = Column(String(100), unique=True, nullable=False)  # Email deve ser único e limitado a 100 caracteres
    preferencias_tom = Column(String(50), nullable=False)  # Limite de 50 caracteres para tom (sarcastico, compreensivo, etc)
    idioma_preferido = Column(String(10), nullable=False)  # Idioma preferido com limite de 10 caracteres (ex: "pt", "en")

    # Relacionamento com a tabela Prompt
    prompts = relationship('Prompt', back_populates='usuario')


# Classe Recebimento
class Recebimento(Base):
    __tablename__ = 'recebimentos'
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela se já existir
    id = Column(Integer, primary_key=True)
    categoria = Column(String(50), nullable=False)
    valor = Column(Float, nullable=False)
    total_custos = Column(Float, nullable=False)
    receita_projetada = Column(Float, nullable=False)
    data_recebimento = Column(DateTime, default=datetime.datetime.now)


# Classe Prompt
class Prompt(Base):
    __tablename__ = 'prompts'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    texto = Column(Text, nullable=False)  # Texto do prompt enviado pelo usuário
    resposta = Column(Text, nullable=False)  # Resposta gerada pela IA
    categoria = Column(String(50), nullable=False, default="geral")  # Categoria do prompt (ex: geral, finanças)
    origem_resposta = Column(String(50), nullable=False, default="local")  # Origem da resposta (ex: local, GPT-4)
    data_criacao = Column(DateTime, default=datetime.datetime.now)

    # Relacionamento com a tabela Usuario
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship('Usuario', back_populates='prompts')

    # Relacionamento com as análises
    analises = relationship('Analise', back_populates='prompt')

    # Relacionamento com as respostas da GPT-4
    gpt4_responses = relationship('GPT4Response', back_populates='prompt')


# Classe GPT4Response (para armazenar respostas específicas da GPT-4)
class GPT4Response(Base):
    __tablename__ = 'gpt4_responses'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    prompt_id = Column(Integer, ForeignKey('prompts.id'))  # Relacionamento com a tabela Prompt
    resposta_gpt4 = Column(Text, nullable=False)  # Resposta da GPT-4
    data_resposta = Column(DateTime, default=datetime.datetime.now)

    # Relacionamento com a tabela Prompt
    prompt = relationship('Prompt', back_populates='gpt4_responses')


# Classe Analise (para armazenar análises feitas sobre os prompts)
class Analise(Base):
    __tablename__ = 'analises'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    tipo_analise = Column(String(50), nullable=False)  # Ex: 'financeira', 'geral', 'humor'
    resultado = Column(Text, nullable=False)  # Armazena o relatório ou resultado da análise
    data_analise = Column(DateTime, default=datetime.datetime.now)

    # Relacionamento com a tabela Prompt
    prompt_id = Column(Integer, ForeignKey('prompts.id'))
    prompt = relationship('Prompt', back_populates='analises')


# Configuração do motor do banco de dados
# Aqui, usamos SQLite, mas você pode mudar para outro banco (como MySQL, PostgreSQL, etc.)
engine = create_engine('sqlite:///db.sqlite')


# Função para criar todas as tabelas no banco de dados
def criar_tabelas():
    """Cria todas as tabelas no banco de dados."""
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso.")
