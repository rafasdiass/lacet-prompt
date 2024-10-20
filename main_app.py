import sys
import os
from dearpygui.dearpygui import *  # Importando a nova API do Dear PyGui
from app_balance.gui_app import MainWindow
from app_balance.users.user_creation_dialog import UserCreationDialog
from app_balance.processamento.models import criar_tabelas
from app_balance.users.user_preferences_service import UserPreferencesService
import sqlite3

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

if __name__ == "__main__":
    main()
