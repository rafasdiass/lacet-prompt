from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QLineEdit, QTextEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
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

        # Configuração dos botões com estilos corrigidos
        button_style = """
            QPushButton {
                background-color: #E6E6FA;  /* Cor pastel */
                color: black;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                min-width: 300px;  /* Todos os botões têm a mesma largura */
            }
            QPushButton:hover {
                background-color: #D8BFD8;  /* Hover em uma cor pastel mais escura */
            }
        """

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

        # Campo de input no rodapé com ícone de envio
        footer_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Digite sua pergunta para a Catelina Lacet...")
        self.input_field.setStyleSheet("font-size: 16px; padding: 10px;")
        self.input_field.setMinimumHeight(50)

        # Botão de envio dentro do campo de input
        send_button = QPushButton()
        send_button.setIcon(QIcon(qtawesome.icon('fa.send', color='black')))
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #E6E6FA;
                border-radius: 8px;
                padding: 10px;
                min-width: 50px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #D8BFD8;
            }
        """)
        send_button.clicked.connect(self.enviar_pergunta)

        # Adiciona o campo de input e o botão de envio no rodapé
        footer_layout.addWidget(self.input_field)
        footer_layout.addWidget(send_button)
        layout.addLayout(footer_layout)

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
