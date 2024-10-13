# -*- coding: utf-8 -*-
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
    data = Column(DateTime, default=datetime.now, nullable=False)  # Data do envio do prompt

    def __repr__(self):
        return f"<Prompt(id={self.id}, conteudo={self.conteudo}, data={self.data})>"

# Para criar as tabelas no banco de dados, basta rodar o comando apropriado
# session = Session()
# Base.metadata.create_all(engine)
