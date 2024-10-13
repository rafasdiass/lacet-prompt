from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Configuração do banco de dados SQLite
DATABASE_URL = 'sqlite:///recebimentos.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Base declarativa
Base = declarative_base()

# Definindo o modelo Recebimento
class Recebimento(Base):
    __tablename__ = 'recebimentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    valor = Column(Float, nullable=False)
    categoria = Column(String, nullable=True)  # Categoria opcional
    descricao = Column(String, nullable=True)  # Descrição opcional

    def __repr__(self):
        return f"<Recebimento(id={self.id}, data={self.data}, valor={self.valor})>"

# Definindo o modelo Despesa
class Despesa(Base):
    __tablename__ = 'despesas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    valor = Column(Float, nullable=False)
    categoria = Column(String, nullable=True)  # Categoria opcional
    descricao = Column(String, nullable=True)  # Descrição opcional

    def __repr__(self):
        return f"<Despesa(id={self.id}, data={self.data}, valor={self.valor})>"

# Definindo o modelo Prompt
class Prompt(Base):
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    conteudo = Column(String, nullable=False)
    resposta = Column(String, nullable=True)
    data = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Prompt(id={self.id}, conteudo={self.conteudo}, data={self.data})>"

# Definindo o modelo Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preferencias_tom = Column(String, default="casual")
    idioma_preferido = Column(String, default="pt")
    data_registro = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Usuario(id={self.id}, nome={self.nome}, preferencias_tom={self.preferencias_tom}, idioma_preferido={self.idioma_preferido})>"

# Função para criar as tabelas no banco de dados
def criar_tabelas():
    Base.metadata.create_all(engine)
    print("Banco de dados configurado e tabelas criadas com sucesso!")
