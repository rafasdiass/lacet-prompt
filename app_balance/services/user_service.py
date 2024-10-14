# user_service.py
from sqlalchemy.exc import SQLAlchemyError
from app_balance.processamento.models import Usuario
from app_balance.processamento.database_setup import Session

class UserService:
    """
    Serviço para gerenciar operações relacionadas ao usuário, como criação e consulta.
    """

    def __init__(self):
        self.session = Session()

    def criar_usuario(self, nome, email, preferencias_tom="padrao", idioma_preferido="pt"):
        """
        Cria um novo usuário no banco de dados ou retorna um existente.
        
        Args:
            nome (str): Nome do usuário.
            email (str): Email do usuário (deve ser único).
            preferencias_tom (str): Preferência de tom de humor (ex: 'sarcástico').
            idioma_preferido (str): Idioma preferido do usuário.

        Returns:
            Usuario: O objeto de usuário criado ou já existente.
        """
        try:
            # Verifica se o usuário já existe
            usuario = self.session.query(Usuario).filter_by(email=email).first()
            if not usuario:
                # Cria um novo usuário caso não exista
                usuario = Usuario(
                    nome=nome,
                    email=email,
                    preferencias_tom=preferencias_tom,
                    idioma_preferido=idioma_preferido
                )
                self.session.add(usuario)
                self.session.commit()
                print(f"Usuário '{nome}' criado com sucesso.")
            else:
                print(f"Usuário '{nome}' já existe no sistema.")
            return usuario
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Erro ao criar ou carregar o usuário: {str(e)}")

    def obter_usuario_por_email(self, email):
        """
        Retorna o usuário baseado no email.
        
        Args:
            email (str): Email do usuário.

        Returns:
            Usuario: O objeto de usuário ou None se não encontrado.
        """
        try:
            usuario = self.session.query(Usuario).filter_by(email=email).first()
            return usuario
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro ao buscar o usuário: {str(e)}")

    def atualizar_preferencia_humor(self, email, humor):
        """
        Atualiza a preferência de humor de um usuário.

        Args:
            email (str): Email do usuário.
            humor (str): Novo humor a ser definido.
        """
        try:
            usuario = self.obter_usuario_por_email(email)
            if usuario:
                usuario.preferencias_tom = humor
                self.session.commit()
                print(f"Humor do usuário '{usuario.nome}' atualizado para: {humor}")
            else:
                raise RuntimeError(f"Usuário com email '{email}' não encontrado.")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Erro ao atualizar o humor do usuário: {str(e)}")

    def fechar_sessao(self):
        """
        Fecha a sessão atual do banco de dados.
        """
        self.session.close()
