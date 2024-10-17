import sys
import os
from PyQt5.QtWidgets import QApplication
from app_balance.gui_app import MainWindow
from app_balance.users.user_creation_dialog import UserCreationDialog
from app_balance.users.login_dialog import LoginDialog
from app_balance.processamento.models import criar_tabelas
from app_balance.users.user_preferences_service import UserPreferencesService
from services.persistencia import DataPersistenceService
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados
DATABASE_URL = 'sqlite:///db.sqlite'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def verificar_tabelas():
    """Função para verificar se as tabelas foram criadas corretamente no banco de dados."""
    if os.path.exists('db.sqlite'):
        print("Banco de dados encontrado.")
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios';")
        tabelas = cursor.fetchall()
        if not tabelas:
            print("Tabela 'usuarios' não encontrada, criando tabelas...")
            criar_tabelas()  # Criação de todas as tabelas
        else:
            print("Tabelas já estão presentes.")
        conn.close()
    else:
        print("Banco de dados não encontrado. Criando novo banco de dados.")
        criar_tabelas()

def main():
    verificar_tabelas()  # Verifica e garante que as tabelas estejam criadas antes de iniciar o app

    app = QApplication(sys.argv)

    # Inicializa o serviço de preferências do usuário
    user_service = UserPreferencesService(session)

    while True:
        # Exibe a tela de login primeiro
        login_dialog = LoginDialog(user_service)
        if login_dialog.exec_():  # Se o login for bem-sucedido
            usuario = user_service.carregar_usuario_existente(login_dialog.name_input.text())
            if usuario:
                # Integrando o DataPersistenceService
                data_service = DataPersistenceService(session, usuario)  # Inicializa o serviço de persistência

                # Inicializa a tela principal com o usuário autenticado e o serviço de persistência
                window = MainWindow(usuario, data_service)  # Passa o data_service para a MainWindow
                window.show()
                sys.exit(app.exec_())
        else:
            # Se o login não for bem-sucedido ou o usuário clicar em criar conta
            user_dialog = UserCreationDialog(user_service)
            if user_dialog.exec_():  # Se o usuário for criado com sucesso
                continue  # Retorna à tela de login

if __name__ == "__main__":
    main()
