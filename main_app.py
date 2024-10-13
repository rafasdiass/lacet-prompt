# main_app.py
import sys
from PyQt5.QtWidgets import QApplication
from app_balance.gui_app import MainWindow
from app_balance.models import criar_tabelas

def main():
    criar_tabelas()  # Garante que as tabelas sejam criadas antes de iniciar o app
    app = QApplication(sys.argv)
    window = MainWindow()  # Instancia o MainWindow que está no arquivo gui_app.py
    window.show()  # Exibe a janela
    sys.exit(app.exec_())  # Inicia o loop de eventos da interface gráfica

if __name__ == "__main__":
    main()  # Chama a função principal
