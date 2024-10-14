from sqlalchemy import Column, Integer, String
from processamento.database_setup import Base  # Certifique-se de importar o Base corretamente

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)  # Limite de 50 caracteres
    email = Column(String(100), unique=True, nullable=False)  # Email deve ser único e limitado a 100 caracteres
    preferencias_tom = Column(String(50), nullable=False)  # Adicionado limite de 50 caracteres
    idioma_preferido = Column(String(10), nullable=False)  # Adicionado limite de 10 caracteres (ex: "pt", "en")
