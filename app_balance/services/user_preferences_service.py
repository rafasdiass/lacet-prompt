from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app_balance.models import Usuario  # Modelo para salvar e gerenciar as preferências do usuário
from sqlalchemy.exc import SQLAlchemyError

# Configuração do banco de dados
DATABASE_URL = 'sqlite:///recebimentos.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class UserPreferencesService:
    """
    Serviço para gerenciar as preferências do usuário, como tipo de humor e outras configurações.
    """

    def __init__(self):
        # Carregar as preferências do usuário padrão (Catherine Dean)
        self.usuario = self.carregar_usuario_padrao()

    def carregar_usuario_padrao(self):
        """
        Carrega o usuário padrão 'Catherine Dean' do banco de dados. Se não existir, cria.
        """
        try:
            usuario = session.query(Usuario).filter_by(nome="Catherine Dean").first()
            if not usuario:
                # Criar usuário padrão
                usuario = Usuario(nome="Catherine Dean", preferencias_tom="padrao", idioma_preferido="pt")
                session.add(usuario)
                session.commit()
                print("Usuário 'Catherine Dean' criado com sucesso.")
            return usuario
        except SQLAlchemyError as e:
            session.rollback()
            raise RuntimeError(f"Erro ao carregar ou criar o usuário padrão: {str(e)}")

    def set_humor(self, humor: str):
        """
        Define o humor do usuário e salva no banco de dados.
        """
        try:
            self.usuario.preferencias_tom = humor
            session.commit()
            print(f"Humor alterado para: {humor}")
        except SQLAlchemyError as e:
            session.rollback()
            raise RuntimeError(f"Erro ao salvar as preferências de humor no banco de dados: {str(e)}")

    def get_humor_atual(self):
        """
        Retorna o humor atual do usuário.
        """
        return self.usuario.preferencias_tom
