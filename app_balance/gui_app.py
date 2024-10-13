from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QLineEdit, QTextEdit, QHBoxLayout, QDialog, QComboBox, QDialogButtonBox
from PyQt5.QtCore import Qt, QSize  # Importando QSize corretamente
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

        # Inicializando variáveis para armazenar dados
        self.custos = None
        self.receita_projetada = None

        # Inicializando a interface de usuário
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Criar layout para o botão de mudança de humor no topo direito
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # Adiciona espaço à esquerda

        # Botão de mudar o humor - no canto superior direito
        self.mudar_humor_button = QPushButton()
        self.mudar_humor_button.setIcon(qtawesome.icon('fa.gear', color='white'))
        self.mudar_humor_button.setIconSize(QSize(40, 40))  # Aumentando o tamanho do ícone corretamente
        self.mudar_humor_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                color: #FFD700;  /* Cor mais clara e visível no hover */
            }
        """)
        self.mudar_humor_button.clicked.connect(self.abrir_modal_humor)
        top_layout.addWidget(self.mudar_humor_button, alignment=Qt.AlignRight)
        layout.addLayout(top_layout)  # Adiciona o layout de topo ao layout principal

        # Mensagem de boas-vindas
        self.welcome_message = QLabel("Bem-vindo, Cath Dean! Show-me the money! Vamos começar a trabalhar...")
        self.welcome_message.setAlignment(Qt.AlignCenter)
        self.welcome_message.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFD700; margin-bottom: 20px;")
        layout.addWidget(self.welcome_message)

        # Adicionando o logotipo
        self.logo = QLabel()
        pixmap = QPixmap('assets/LOGO-BRANCA.PNG')
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setFixedSize(400, 150)  # Reduzindo o tamanho da logo
        self.logo.setScaledContents(True)  # Mantém a qualidade ao redimensionar
        layout.addWidget(self.logo)

        # Criar layout horizontal para os botões centrais
        button_layout = QHBoxLayout()

        # Configuração dos botões com estilos corrigidos e margem superior
        button_style = """
            QPushButton {
                background-color: #E6E6FA;  /* Cor pastel */
                color: black;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                min-width: 250px;
                margin-top: 20px;  /* Adicionando margem superior */
            }
            QPushButton:hover {
                background-color: #D8BFD8;  /* Hover em uma cor pastel mais escura */
            }
        """

        # Botão de upload de arquivos (PDF, Excel, DOCX)
        self.upload_button = QPushButton("Enviar Arquivo")
        self.upload_button.setIcon(qtawesome.icon('fa.upload', color='black'))
        self.upload_button.setStyleSheet(button_style)
        self.upload_button.clicked.connect(self.upload_file)
        button_layout.addWidget(self.upload_button)

        # Botão para análise de custos (inicialmente desabilitado)
        self.analyze_cost_button = QPushButton("Análise de Custos")
        self.analyze_cost_button.setIcon(qtawesome.icon('fa.money', color='black'))
        self.analyze_cost_button.setStyleSheet(button_style)
        self.analyze_cost_button.setEnabled(False)  # Desabilitado até que os dados estejam disponíveis
        self.analyze_cost_button.clicked.connect(self.analyze_costs)
        button_layout.addWidget(self.analyze_cost_button)

        # Botão para análise de investimentos (também desabilitado inicialmente)
        self.analyze_investment_button = QPushButton("Análise de Investimentos")
        self.analyze_investment_button.setIcon(qtawesome.icon('fa.line-chart', color='black'))
        self.analyze_investment_button.setStyleSheet(button_style)
        self.analyze_investment_button.setEnabled(False)  # Desabilitado até que os dados estejam disponíveis
        self.analyze_investment_button.clicked.connect(self.analyze_investments)
        button_layout.addWidget(self.analyze_investment_button)

        layout.addLayout(button_layout)

        # Campo de exibição dos resultados
        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        # Campo de input no rodapé com ícone de envio
        footer_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Digite sua pergunta para a Catelina Lacet...")
        self.input_field.setStyleSheet("font-size: 16px; padding: 20px; background-color: #A9A9A9;")  # Campo de input maior e fundo cinza
        self.input_field.setMinimumHeight(80)  # Aumenta o tamanho do campo de input

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

    def abrir_modal_humor(self):
        """Abre um modal para o usuário selecionar o humor."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Selecione o Humor")
        dialog.setFixedSize(300, 200)

        layout = QVBoxLayout()

        # ComboBox para seleção do humor
        humor_combo = QComboBox(dialog)
        humor_combo.addItems(['Padrão', 'Sarcastico', 'Compreensivo'])
        layout.addWidget(humor_combo)

        # Botões para confirmar ou cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.set_humor(humor_combo.currentText(), dialog))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec_()

    def set_humor(self, humor: str, dialog: QDialog):
        """Define o humor com base na escolha do usuário."""
        self.user_preferences_service.set_humor(humor.lower())
        self.result_display.setText(f"Humor alterado para: {humor}")
        dialog.accept()

    def upload_file(self):
        """Permite o upload de arquivos PDF, Excel ou DOCX para processamento."""
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione um arquivo", "", "Documentos (*.pdf *.xlsx *.docx)")

        if file_path:
            try:
                file_type = file_path.split('.')[-1].lower()  # Detectar o tipo de arquivo
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                
                # Processa o arquivo e armazena os dados de custos e receita
                resultado = self.file_service.processar_arquivo(file_data, file_type)
                self.custos = resultado['categorias_custos']
                self.receita_projetada = resultado['receita_projetada']

                self.result_display.setText(f"Arquivo processado com sucesso:\n{resultado}")
                
                # Habilitar botões de análise
                self.analyze_cost_button.setEnabled(True)
                self.analyze_investment_button.setEnabled(True)
            except Exception as e:
                self.result_display.setText(f"Erro ao processar o arquivo: {str(e)}")

    def analyze_costs(self):
        """Analisa os dados reais de custos e exibe o resultado."""
        if self.custos and self.receita_projetada:
            resposta = self.gpt_service.analyze_costs(self.custos, self.receita_projetada)
            self.result_display.setText(resposta)

    def analyze_investments(self):
        """Analisa os dados reais de investimentos e exibe o resultado."""
        resposta = self.gpt_service.analyze_investments()
        self.result_display.setText(resposta)
