# -*- coding: utf-8 -*-
"""Script para criar o banco de dados SQLite com tabelas de recebimentos e despesas."""

from sqlalchemy import create_engine, Column, Integer, Float, Date, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuração do SQLite
DATABASE_URL = 'sqlite:///recebimentos.db'

# Configurar a engine e a sessão para o SQLite
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Base declarativa para as classes do modelo
Base = declarative_base()

# Definir a tabela de recebimentos
class Recebimento(Base):
    __tablename__ = 'recebimentos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    valor = Column(Float, nullable=False)
    categoria = Column(String, nullable=True)  # Categoria opcional para os recebimentos
    descricao = Column(String, nullable=True)  # Descrição opcional para detalhes extras

# Definir a tabela de despesas
class Despesa(Base):
    __tablename__ = 'despesas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    valor = Column(Float, nullable=False)
    categoria = Column(String, nullable=True)  # Categoria opcional para as despesas (ex: pessoal, alimentação)
    descricao = Column(String, nullable=True)  # Descrição detalhada da despesa

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)

print("Banco de dados e tabelas 'recebimentos' e 'despesas' criados com sucesso!")
