# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from typing import Optional, Type, TypeVar
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.exc import SQLAlchemyError

# Configuração do banco de dados SQLite
DATABASE_URL = 'sqlite:///recebimentos.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Base declarativa
Base = declarative_base()

# Tipo genérico para métodos CRUD
T = TypeVar("T", bound="PkModel")

class CRUDMixin:
    """Mixin que adiciona métodos convenientes para operações CRUD."""

    @classmethod
    def create(cls, **kwargs):
        """Cria um novo registro e salva no banco de dados."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Atualiza campos específicos de um registro."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            return self.save()
        return self

    def save(self, commit=True):
        """Salva o registro no banco de dados."""
        session.add(self)
        if commit:
            try:
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                raise
        return self

    def delete(self, commit=True):
        """Remove o registro do banco de dados."""
        session.delete(self)
        if commit:
            try:
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                raise
        return self


class Model(CRUDMixin, Base):
    """Modelo base que inclui métodos CRUD convenientes."""
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        """Gera o nome da tabela automaticamente com base no nome da classe."""
        return cls.__name__.lower()

class PkModel(Model):
    """Modelo base que adiciona uma coluna de chave primária chamada 'id'."""
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get_by_id(cls: Type[T], record_id) -> Optional[T]:
        """Busca um registro pelo ID."""
        if isinstance(record_id, (int, float, str)) and str(record_id).isdigit():
            return session.get(cls, int(record_id))
        return None


def reference_col(tablename, nullable=False, pk_name="id", **kwargs):
    """Cria uma coluna de referência de chave estrangeira."""
    return Column(ForeignKey(f"{tablename}.{pk_name}"), nullable=nullable, **kwargs)


# Exemplo de modelo de uso
class Recebimento(PkModel):
    """Modelo de Recebimento."""
    data = Column(String, nullable=False)
    valor = Column(Integer, nullable=False)
    categoria = Column(String, nullable=True)
    descricao = Column(String, nullable=True)

# Exemplo de relacionamento
class Categoria(PkModel):
    """Modelo de Categoria que será referenciada."""
    nome = Column(String, nullable=False)

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)

print("Banco de dados configurado e tabelas criadas com sucesso!")
