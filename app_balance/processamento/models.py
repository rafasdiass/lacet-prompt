from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from processamento.database_setup import Base
import datetime

class Recebimento(Base):
    __tablename__ = 'recebimentos'
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela se já existir
    id = Column(Integer, primary_key=True)
    categoria = Column(String(50), nullable=False)
    valor = Column(Float, nullable=False)
    total_custos = Column(Float, nullable=False)
    receita_projetada = Column(Float, nullable=False)
    data_recebimento = Column(DateTime, default=datetime.datetime.now)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    prompts = relationship('Prompt', back_populates='usuario')

class Prompt(Base):
    __tablename__ = 'prompts'
    id = Column(Integer, primary_key=True)
    texto = Column(Text, nullable=False)
    resposta = Column(Text, nullable=False)
    categoria = Column(String(50), nullable=False, default="geral")  # Nova coluna para categorizar o tipo de prompt/resposta
    origem_resposta = Column(String(50), nullable=False, default="local")
    data_criacao = Column(DateTime, default=datetime.datetime.now)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship('Usuario', back_populates='prompts')
    analises = relationship('Analise', back_populates='prompt')

class GPT4Response(Base):
    __tablename__ = 'gpt4_responses'
    id = Column(Integer, primary_key=True)
    prompt_id = Column(Integer, ForeignKey('prompts.id'))
    resposta_gpt4 = Column(Text, nullable=False)
    data_resposta = Column(DateTime, default=datetime.datetime.now)
    prompt = relationship('Prompt', back_populates='gpt4_responses')

class Analise(Base):
    __tablename__ = 'analises'
    id = Column(Integer, primary_key=True)
    tipo_analise = Column(String(50), nullable=False)  # Ex: 'financeira', 'geral', 'humor'
    resultado = Column(Text, nullable=False)  # Armazena o relatório ou resultado da análise
    data_analise = Column(DateTime, default=datetime.datetime.now)
    prompt_id = Column(Integer, ForeignKey('prompts.id'))
    prompt = relationship('Prompt', back_populates='analises')

# Relacionamentos entre as tabelas
Prompt.gpt4_responses = relationship('GPT4Response', order_by=GPT4Response.id, back_populates='prompt')
Prompt.analises = relationship('Analise', order_by=Analise.id, back_populates='prompt')
