from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Declarative base para criar modelos do SQLAlchemy
Base = declarative_base()

class Recebimento(Base):
    """
    Modelo que representa os dados de um recebimento.
    """
    __tablename__ = 'recebimentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)  # Data do recebimento
    valor = Column(Float, nullable=False)  # Valor do recebimento

    def __repr__(self):
        return f"<Recebimento(id={self.id}, data={self.data}, valor={self.valor})>"

class Prompt(Base):
    """
    Modelo que representa os prompts enviados ao GPT-4.
    """
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    conteudo = Column(String, nullable=False)  # Conteúdo do prompt
    resposta = Column(String, nullable=True)  # Resposta do GPT-4
    data = Column(DateTime, default=datetime.now, nullable=False)  # Data do envio do prompt

    def __repr__(self):
        return f"<Prompt(id={self.id}, conteudo={self.conteudo}, data={self.data})>"

class Usuario(Base):
    """
    Modelo que representa as preferências do usuário.
    """
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)  # Nome do usuário
    preferencias_tom = Column(String, default="casual")  # Preferências de tom: 'sarcastico', 'compreensivo', 'padrao'
    idioma_preferido = Column(String, default="pt")  # Idioma preferido: 'pt', 'en'
    data_registro = Column(DateTime, default=datetime.now)  # Data de registro do usuário

    def __repr__(self):
        return f"<Usuario(id={self.id}, nome={self.nome}, preferencias_tom={self.preferencias_tom}, idioma_preferido={self.idioma_preferido})>"
