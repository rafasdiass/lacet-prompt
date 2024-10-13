from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import qtawesome
from app_balance.services.gpt_service import GPTService
from app_balance.services.file_processing_service import FileProcessingService
from app_balance.services.user_preferences_service import UserPreferencesService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catelina Lacet - Sua IA Financeira com Senso de Humor!")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("background-color: #000000; color: #EDEDED;")

        # Inicializando serviços
        self.gpt_service = GPTService()
        self.file_service = FileProcessingService()
        self.user_preferences_service = UserPreferencesService()

        # Inicializando a interface de usuário
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Adicionando o logotipo
        self.logo = QLabel()
        pixmap = QPixmap('assets/LOGO-BRANCA.PNG')
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setFixedSize(400, 150)  # Reduzindo o tamanho da logo
        self.logo.setScaledContents(True)  # Mantém a qualidade ao redimensionar
        layout.addWidget(self.logo)

        # Campo de input para interação com a IA
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Digite sua pergunta para a Catelina Lacet...")
        layout.addWidget(self.input_field)

        # Configuração dos botões com estilos corrigidos
        button_style = """
            QPushButton {
                background-color: #F8F4E3;
                color: black;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                max-width: 300px;  /* Limita a largura dos botões */
            }
            QPushButton:hover {
                background-color: #E0E0E0;  /* Cor ao passar o mouse */
            }
        """

        # Botão de envio de pergunta ao GPT-4
        self.gpt_button = QPushButton("Enviar Pergunta")
        self.gpt_button.setStyleSheet(button_style)
        self.gpt_button.clicked.connect(self.enviar_pergunta)
        layout.addWidget(self.gpt_button, alignment=Qt.AlignCenter)

        # Botão de mudar o humor
        self.mudar_humor_button = QPushButton("Humor")
        self.mudar_humor_button.setIcon(qtawesome.icon('fa.gear'))
        self.mudar_humor_button.setStyleSheet(button_style)
        self.mudar_humor_button.clicked.connect(self.mudar_humor)
        layout.addWidget(self.mudar_humor_button, alignment=Qt.AlignCenter)

        # Botão de upload de arquivos (PDF, Excel, DOCX)
        self.upload_button = QPushButton("Enviar Arquivo")
        self.upload_button.setIcon(qtawesome.icon('fa.upload'))
        self.upload_button.setStyleSheet(button_style)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)

        # Botão para análise de custos (simulação)
        self.analyze_cost_button = QPushButton("Análise de Custos")
        self.analyze_cost_button.setIcon(qtawesome.icon('fa.money', color='black'))
        self.analyze_cost_button.setStyleSheet(button_style)
        self.analyze_cost_button.clicked.connect(self.analyze_costs)
        layout.addWidget(self.analyze_cost_button, alignment=Qt.AlignCenter)

        # Campo de exibição dos resultados
        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def enviar_pergunta(self):
        """Envia a pergunta digitada ao GPT-4 e exibe a resposta."""
        prompt = self.input_field.text()
        resposta = self.gpt_service.enviar_prompt(prompt)
        self.result_display.setText(resposta)

    def mudar_humor(self):
        """Altera o humor e exibe a nova configuração."""
        novo_humor = self.user_preferences_service.mudar_humor()
        self.result_display.setText(f"Humor alterado para: {novo_humor}")

    def upload_file(self):
        """Permite o upload de arquivos PDF, Excel ou DOCX para processamento."""
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione um arquivo", "", "Documentos (*.pdf *.xlsx *.docx)")

        if file_path:
            try:
                file_type = file_path.split('.')[-1].lower()  # Detectar o tipo de arquivo
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                resposta_gpt = self.file_service.processar_arquivo(file_data, file_type)
                self.result_display.setText(f"Arquivo processado com sucesso:\n{resposta_gpt}")
            except Exception as e:
                self.result_display.setText(f"Erro ao processar o arquivo: {str(e)}")

    def analyze_costs(self):
        """Simula a análise de custos e exibe o resultado."""
        custos = {
            'total_custos': 10000,
            'valor_hora': 120.0,
            'categorias_custos': {'Serviços': 4000, 'Infraestrutura': 2000, 'Funcionários': 4000}
        }
        receita_projetada = 15000
        resposta = self.gpt_service.analyze_costs(custos, receita_projetada)
        self.result_display.setText(resposta)
