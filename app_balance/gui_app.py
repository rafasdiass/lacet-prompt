from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QLineEdit, QTextEdit, QHBoxLayout, QMessageBox, QScrollArea
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
import qtawesome
from app_balance.services.gpt_service import GPTService
from app_balance.services.file_processing_service import FileProcessingService
from app_balance.services.user_preferences_service import UserPreferencesService
from app_balance.models import Recebimento
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Configuração do banco de dados
DATABASE_URL = 'sqlite:///recebimentos.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catelina Lacet - Sua IA Financeira com Senso de Humor!")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("background-color: #000000; color: #EDEDED; font-family: 'Arial', sans-serif;")

        # Inicializando serviços
        self.gpt_service = GPTService()
        self.file_service = FileProcessingService()
        self.user_preferences_service = UserPreferencesService()

        # Estado inicial do humor
        self.humores = ['padrao', 'compreensivo', 'sarcastico']
        self.humor_index = 0

        # Inicializando a interface de usuário
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Criar layout para o botão de mudança de humor no topo direito
        top_layout = QHBoxLayout()
        top_layout.addStretch()

        # Botão de mudar o humor - no canto superior direito
        self.humor_button = QPushButton()
        self.humor_button.setIcon(self.get_humor_icon())
        self.humor_button.setIconSize(QSize(40, 40))
        self.humor_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 10px;
                margin: 10px;
            }
        """)
        self.humor_button.clicked.connect(self.cycle_humor)
        top_layout.addWidget(self.humor_button, alignment=Qt.AlignRight)
        layout.addLayout(top_layout)

        # Adicionando o logotipo centralizado
        logo_layout = QVBoxLayout()
        self.logo = QLabel()
        pixmap = QPixmap('assets/LOGO-BRANCA.PNG')
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setFixedSize(150, 50)  # Reduzindo o tamanho da logo
        self.logo.setScaledContents(True)
        logo_layout.addWidget(self.logo)
        layout.addLayout(logo_layout)

        # Área de texto de conversas com rolagem
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("background-color: #2E2E2E; color: white; font-size: 16px; padding: 10px;")
        scroll_area.setWidget(self.result_display)
        layout.addWidget(scroll_area)

        # Primeira mensagem de boas-vindas da IA
        self.result_display.append(f"<p style='color: yellow;'>Catelina Lacet: {self.get_dynamic_welcome_message()}</p>")

        # Criar layout horizontal para o campo de input e botões
        input_layout = QHBoxLayout()

        # Campo de input de texto
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Digite sua pergunta para a Catelina Lacet...")
        self.input_field.setStyleSheet("font-size: 16px; padding: 10px; background-color: #696969; color: white;")
        self.input_field.setMinimumHeight(60)  # Aumentando o tamanho do campo de input
        input_layout.addWidget(self.input_field)

        # Botões ao lado do campo de input
        send_button = QPushButton()
        send_button.setIcon(QIcon(qtawesome.icon('fa.send', color='black')))
        send_button.setIconSize(QSize(30, 30))
        send_button.setStyleSheet("background-color: #E6E6FA; border-radius: 8px;")
        send_button.clicked.connect(self.enviar_pergunta)
        input_layout.addWidget(send_button)

        self.analyze_cost_button = QPushButton()
        self.analyze_cost_button.setIcon(QIcon(qtawesome.icon('fa.money', color='black')))
        self.analyze_cost_button.setIconSize(QSize(30, 30))
        self.analyze_cost_button.setStyleSheet("background-color: #C0C0C0; border-radius: 8px;")
        self.analyze_cost_button.setEnabled(True)
        self.analyze_cost_button.clicked.connect(self.mensagem_arquivo_necessario)
        input_layout.addWidget(self.analyze_cost_button)

        self.analyze_investment_button = QPushButton()
        self.analyze_investment_button.setIcon(QIcon(qtawesome.icon('fa.line-chart', color='black')))
        self.analyze_investment_button.setIconSize(QSize(30, 30))
        self.analyze_investment_button.setStyleSheet("background-color: #C0C0C0; border-radius: 8px;")
        self.analyze_investment_button.setEnabled(True)
        self.analyze_investment_button.clicked.connect(self.mensagem_arquivo_necessario)
        input_layout.addWidget(self.analyze_investment_button)

        upload_button = QPushButton()
        upload_button.setIcon(QIcon(qtawesome.icon('fa.upload', color='black')))
        upload_button.setIconSize(QSize(30, 30))
        upload_button.setStyleSheet("background-color: #E6E6FA; border-radius: 8px;")
        upload_button.clicked.connect(self.upload_file)
        input_layout.addWidget(upload_button)

        layout.addLayout(input_layout)

        # Definir o widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def enviar_pergunta(self):
        """Envia a pergunta digitada ao GPT-4 e exibe a resposta, priorizando dados locais."""
        prompt = self.input_field.text()
        resposta = self.gpt_service.enviar_prompt(prompt)
        self.result_display.append(f"<p style='color: cyan;'>Você: {prompt}</p>")
        self.result_display.append(f"<p style='color: yellow;'>Catelina Lacet: {resposta}</p>")
        self.input_field.clear()

    def cycle_humor(self):
        """Troca o humor e atualiza o ícone e a mensagem de boas-vindas."""
        self.humor_index = (self.humor_index + 1) % len(self.humores)
        humor = self.humores[self.humor_index]
        self.user_preferences_service.set_humor(humor)
        self.humor_button.setIcon(self.get_humor_icon())
        humor_message = self.get_dynamic_welcome_message()
        self.result_display.append(f"<p style='color: yellow;'>Catelina Lacet: {humor_message}</p>")

    def get_humor_icon(self):
        """Retorna o ícone correspondente ao humor atual."""
        humor = self.humores[self.humor_index]
        if humor == 'sarcastico':
            return QIcon(qtawesome.icon('fa.frown-o', color='red'))  # Zangado
        elif humor == 'compreensivo':
            return QIcon(qtawesome.icon('fa.smile-o', color='green'))  # Sorriso leve
        else:
            return QIcon(qtawesome.icon('fa.smile-o', color='yellow'))  # Sorriso largo (padrão)

    def upload_file(self):
        """Permite o upload de arquivos PDF, Excel ou DOCX para processamento."""
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione um arquivo", "", "Documentos (*.pdf *.xlsx *.docx)")

        if file_path:
            try:
                file_type = file_path.split('.')[-1].lower()
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                resposta_gpt = self.file_service.processar_arquivo(file_data, file_type)
                self.result_display.append(f"<p style='color: white;'>Arquivo processado com sucesso:\n{resposta_gpt}</p>")
                # Habilitar os botões de análise após o envio do arquivo
                self.analyze_cost_button.setEnabled(True)
                self.analyze_cost_button.setStyleSheet("background-color: #E6E6FA;")
                self.analyze_investment_button.setEnabled(True)
                self.analyze_investment_button.setStyleSheet("background-color: #E6E6FA;")
            except Exception as e:
                self.result_display.append(f"<p style='color: red;'>Erro ao processar o arquivo: {str(e)}</p>")

    def mensagem_arquivo_necessario(self):
        """Exibe mensagem quando tentam usar botões desativados."""
        self.result_display.append("<p style='color: red;'>É necessário enviar os arquivos antes de realizar a análise.</p>")

    def get_dynamic_welcome_message(self):
        """Retorna uma mensagem de boas-vindas dinâmica com base no humor atual."""
        humor = self.user_preferences_service.get_humor_atual()
        if humor == 'sarcastico':
            return "Prepare-se para aprender mais sobre finanças... se é que você entende algo disso."
        elif humor == 'compreensivo':
            return "Vamos juntos conquistar sua estabilidade financeira com calma e paciência."
        else:
            return "Vamos começar a jornada para dominar suas finanças!"
