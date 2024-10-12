# -*- coding: utf-8 -*-
"""Script para criar o banco de dados SQLite e a tabela de recebimentos."""

from sqlalchemy import create_engine, Column, Integer, Float, Date
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

# Criar a tabela no banco de dados
Base.metadata.create_all(engine)

print("Banco de dados e tabela 'recebimentos' criados com sucesso!")
