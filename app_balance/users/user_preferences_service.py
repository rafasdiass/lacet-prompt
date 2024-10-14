from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from processamento.models import Usuario  # Certifique-se de que o caminho está correto
from sqlalchemy.exc import SQLAlchemyError
import re

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
        # Pergunta ao usuário se deseja criar ou carregar um usuário existente
        if input("Deseja criar um novo usuário? (s/n): ").lower() == 's':
            self.usuario = self.criar_usuario_dinamico()
        else:
            self.usuario = self.carregar_usuario_existente()

    def validar_email(self, email):
        """Valida se o email está no formato correto."""
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Email inválido.")

    def criar_usuario_dinamico(self):
        """
        Cria um novo usuário pedindo os dados diretamente do terminal.
        """
        try:
            nome = input("Digite o nome do usuário: ")
            email = input("Digite o email do usuário: ")

            # Valida o formato do email
            self.validar_email(email)

            preferencias_tom = input("Digite o humor preferido (ex: padrao, sarcástico, compreensivo): ")
            idioma_preferido = input("Digite o idioma preferido (ex: pt, en): ")

            # Verifica se o usuário já existe
            if session.query(Usuario).filter_by(nome=nome).first():
                raise ValueError(f"Usuário com nome '{nome}' já existe.")
            if session.query(Usuario).filter_by(email=email).first():
                raise ValueError(f"Usuário com email '{email}' já existe.")

            # Criar e salvar o novo usuário no banco de dados
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                preferencias_tom=preferencias_tom,
                idioma_preferido=idioma_preferido
            )
            session.add(novo_usuario)
            session.commit()
            print(f"Usuário '{nome}' criado com sucesso.")
            return novo_usuario
        except SQLAlchemyError as e:
            session.rollback()
            raise RuntimeError(f"Erro ao criar o usuário: {str(e)}")
        except ValueError as e:
            print(f"Erro de validação: {str(e)}")

    def carregar_usuario_existente(self):
        """
        Carrega um usuário existente do banco de dados pelo nome.
        """
        try:
            nome = input("Digite o nome do usuário a ser carregado: ")
            usuario = session.query(Usuario).filter_by(nome=nome).first()
            if not usuario:
                print(f"Usuário '{nome}' não encontrado.")
                return None
            print(f"Usuário '{nome}' carregado com sucesso.")
            return usuario
        except SQLAlchemyError as e:
            session.rollback()
            raise RuntimeError(f"Erro ao carregar o usuário: {str(e)}")

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

# Exemplo de uso:
if __name__ == "__main__":
    user_service = UserPreferencesService()
    if user_service.usuario:
        humor_atual = user_service.get_humor_atual()
        print(f"O humor atual de {user_service.usuario.nome} é: {humor_atual}")
