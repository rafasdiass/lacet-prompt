from sqlalchemy import create_engine, Column, Integer, String, DateTime
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

# Importar modelos
from .models import Recebimento, Prompt

# Tabela de Usuários (Catherine Dean por enquanto)
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    preferencias_tom = Column(String, default="padrao")  # Valores possíveis: 'padrao', 'sarcastico', 'compreensivo'
    idioma_preferido = Column(String, default="pt")  # Padrão pt
    data_registro = Column(DateTime, default=datetime.now)

# Criar as tabelas no banco de dados
def criar_tabelas():
    Base.metadata.create_all(engine)
    print("Banco de dados configurado e tabelas criadas com sucesso!")

# Criar o usuário Catherine Dean por padrão, se não existir
def criar_usuario_padrao():
    try:
        usuario_existente = session.query(Usuario).filter_by(nome="Catherine Dean").first()
        if not usuario_existente:
            usuario = Usuario(nome="Catherine Dean", preferencias_tom="padrao", idioma_preferido="pt")
            session.add(usuario)
            session.commit()
            print("Usuário padrão 'Catherine Dean' criado com sucesso!")
        else:
            print("Usuário 'Catherine Dean' já existe.")
    except SQLAlchemyError as e:
        print(f"Erro ao criar usuário padrão: {e}")

# Chamar essa função quando iniciar o app para garantir a criação do usuário
def iniciar_banco_dados():
    try:
        criar_tabelas()
        criar_usuario_padrao()
    except SQLAlchemyError as e:
        print(f"Erro ao configurar o banco de dados: {e}")

# Inicializar banco de dados ao importar este módulo
iniciar_banco_dados()
