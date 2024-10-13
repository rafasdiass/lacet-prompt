# app_balance/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Configuração do banco de dados SQLite
DATABASE_URL = 'sqlite:///recebimentos.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Base declarativa
Base = declarative_base()

# Importar modelos
from .models import Recebimento, Prompt

def criar_tabelas():
    Base.metadata.create_all(engine)
    print("Banco de dados configurado e tabelas criadas com sucesso!")
