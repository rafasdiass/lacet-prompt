import sys
<<<<<<< HEAD
from PyQt5.QtWidgets import QApplication
=======
import os
from dearpygui.dearpygui import *  # Importando a nova API do Dear PyGui
>>>>>>> main
from app_balance.gui_app import MainWindow
from app_balance.users.user_creation_dialog import UserCreationDialog
from app_balance.users.login_dialog import LoginDialog
from app_balance.processamento.models import criar_tabelas
from app_balance.users.user_preferences_service import UserPreferencesService
from services.persistencia import DataPersistenceService
from services.gpt_service import GPTService
from app_balance.services.catelina_lacet import CatelinaLacetGPT
from app_balance.services.text_processing import TextProcessingService
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
    criar_tabelas(engine)  # Passa o engine corretamente

def main():
    verificar_tabelas()  # Verifica e garante que as tabelas estejam criadas antes de iniciar o app

<<<<<<< HEAD
    app = QApplication(sys.argv)

    # Inicializa o serviço de preferências do usuário
    user_service = UserPreferencesService(session)

    while True:
        # Exibe a tela de login primeiro
        login_dialog = LoginDialog(user_service)
        if login_dialog.exec_():  # Se o login for bem-sucedido
            if usuario := user_service.carregar_usuario_existente(
                login_dialog.name_input.text()
            ):
                # Inicializa o serviço GPT
                gpt_service = GPTService(api_key="SUA_OPENAI_API_KEY")

                # Inicializa o Catelina Lacet
                catelina_lacet = CatelinaLacetGPT()

                # Inicializa o TextProcessingService com o GPTService
                text_processor = TextProcessingService(gpt_service=gpt_service)

                # Inicializa o serviço de persistência de dados
                data_service = DataPersistenceService(session, usuario)

                # Inicializa a tela principal com o usuário autenticado e os serviços
                window = MainWindow(usuario, data_service, session, text_processor, catelina_lacet)  # Passando o TextProcessingService e Catelina
                window.show()
                sys.exit(app.exec_())
        else:
            # Se o login não for bem-sucedido ou o usuário clicar em criar conta
            user_dialog = UserCreationDialog(user_service)
            if user_dialog.exec_():  # Se o usuário for criado com sucesso
                continue  # Retorna à tela de login
=======
    # Inicializa o serviço de usuário
    user_service = UserPreferencesService()

    # Exibe a tela de criação de usuário
    user_dialog = UserCreationDialog(user_service)
    if user_dialog.exec_():  # Se o usuário for criado com sucesso
        usuario = user_service.carregar_usuario_existente(user_dialog.name_input.text())
        if usuario:
            # Inicializa a tela principal com o usuário
            window = MainWindow(usuario)
            start_dearpygui(primary_window="Catelina Lacet - Bem-vindo!")  # Inicializa Dear PyGui
>>>>>>> main

if __name__ == "__main__":
    main()
