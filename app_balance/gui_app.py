from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QLineEdit, QTextEdit, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
import qtawesome
from app_balance.services.text_processing import TextProcessingService  # Primeira etapa de processamento
from processamento.file_processing_service import FileProcessingService
from users.user_preferences_service import UserPreferencesService
from app_balance.services.catelina_lacet import CatelinaLacetGPT  # Serviço que toma a decisão final

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catelina Lacet - Sua IA Financeira com Senso de Humor!")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("background-color: #000000; color: #EDEDED; font-family: 'Arial', sans-serif;")

        # Inicializando os serviços
        self.text_processor = TextProcessingService()  # Primeiro processador de texto
        self.file_service = FileProcessingService()
        self.user_preferences_service = UserPreferencesService()
        self.cateline_lacet_gpt = CatelinaLacetGPT()  # Serviço que toma a decisão com base no texto processado

        # Variáveis para armazenar dados do usuário
        self.file_data = None

        # Estado inicial do humor
        self.humores = ['padrao', 'compreensivo', 'sarcastico']
        self.humor_index = 0

        # Inicializando a interface de usuário
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Criar layout para o botão de mudança de humor e logo no topo
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        top_layout.addStretch()

        # Logo no topo
        self.logo = QLabel()
        pixmap = QPixmap('assets/LOGO-BRANCA.PNG')
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignLeft)
        self.logo.setFixedSize(120, 40)
        self.logo.setScaledContents(True)
        top_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Botão de mudar o humor
        self.humor_button = QPushButton()
        self.humor_button.setIcon(self.get_humor_icon())
        self.humor_button.setIconSize(QSize(40, 40))
        self.humor_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0;
                margin: 0;
            }
        """)
        self.humor_button.clicked.connect(self.cycle_humor)
        top_layout.addWidget(self.humor_button, alignment=Qt.AlignRight)

        layout.addLayout(top_layout)

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

        # Campo de input de texto
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Digite sua pergunta para a Catelina Lacet...")
        self.input_field.setStyleSheet("font-size: 16px; padding: 10px; background-color: #696969; color: white;")
        self.input_field.setMinimumHeight(60)
        input_layout.addWidget(self.input_field)

        # Botão de enviar pergunta
        send_button = QPushButton()
        send_button.setIcon(QIcon(qtawesome.icon('fa.paper-plane', color='black')))
        send_button.setIconSize(QSize(30, 30))
        send_button.setStyleSheet("background-color: #E6E6FA; border-radius: 8px;")
        send_button.clicked.connect(self.enviar_pergunta)
        input_layout.addWidget(send_button)

        # Botão de upload de arquivo
        upload_button = QPushButton()
        upload_button.setIcon(QIcon(qtawesome.icon('fa.upload', color='black')))
        upload_button.setIconSize(QSize(30, 30))
        upload_button.setStyleSheet("background-color: #E6E6FA; border-radius: 8px;")
        upload_button.clicked.connect(self.upload_file)
        input_layout.addWidget(upload_button)

        layout.addLayout(input_layout)

        # Botões de análise de custos e análise financeira
        analysis_layout = QHBoxLayout()

        # Botão de análise de custos
        self.analyze_cost_button = QPushButton("Análise de Custos")
        self.analyze_cost_button.setStyleSheet("background-color: #C0C0C0; border-radius: 8px;")
        self.analyze_cost_button.setIcon(QIcon(qtawesome.icon('fa.money', color='black')))
        self.analyze_cost_button.setIconSize(QSize(30, 30))
        self.analyze_cost_button.clicked.connect(self.analyze_cost)
        self.analyze_cost_button.setEnabled(False)
        analysis_layout.addWidget(self.analyze_cost_button)

        # Botão de análise financeira
        self.analyze_financial_button = QPushButton("Análise Financeira")
        self.analyze_financial_button.setStyleSheet("background-color: #C0C0C0; border-radius: 8px;")
        self.analyze_financial_button.setIcon(QIcon(qtawesome.icon('fa.line-chart', color='black')))
        self.analyze_financial_button.setIconSize(QSize(30, 30))
        self.analyze_financial_button.clicked.connect(self.analyze_financial)
        self.analyze_financial_button.setEnabled(False)
        analysis_layout.addWidget(self.analyze_financial_button)

        layout.addLayout(analysis_layout)

        # Definir o widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def enviar_pergunta(self):
        """
        Envia a pergunta para o processamento e gera uma resposta baseada na análise de texto.
        """
        prompt = self.input_field.text()
        try:
            # Primeiro envia o prompt para o processamento de texto
            analysis = self.text_processor.process_prompt(prompt)

            # Exibe a pergunta e o resultado da análise de texto
            self.result_display.append(f"<p style='color: cyan;'>Você: {prompt}</p>")
            self.result_display.append(f"<p style='color: yellow;'>Análise de Texto: {analysis}</p>")

            # Verifica se é uma saudação ou uma pergunta relacionada a finanças
            if self.text_processor.is_greeting(prompt):
                resposta = self.get_greeting_response(analysis)
            else:
                # Continue com a lógica de finanças se palavras-chave estiverem presentes
                resposta = self.cateline_lacet_gpt.generate_response(prompt)

            if resposta:
                self.result_display.append(f"<p style='color: yellow;'>Catelina Lacet: {resposta}</p>")
            else:
                self.result_display.append(f"<p style='color: red;'>Erro ao processar sua pergunta. Tente novamente mais tarde.</p>")
        except Exception as e:
            self.result_display.append(f"<p style='color: red;'>Erro: {str(e)}</p>")
        self.input_field.clear()

    def upload_file(self):
        """
        Faz o upload do arquivo e processa os dados financeiros.
        """
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione um arquivo", "", "Documentos (*.pdf *.xlsx *.docx)")

        if file_path:
            try:
                file_type = file_path.split('.')[-1].lower()
                with open(file_path, 'rb') as f:
                    self.file_data = f.read()
                self.result_display.append(f"<p style='color: cyan;'>Arquivo carregado com sucesso. Pronto para análise!</p>")
                # Habilitar os botões de análise após o envio do arquivo
                self.analyze_cost_button.setEnabled(True)
                self.analyze_financial_button.setEnabled(True)
                self.analyze_cost_button.setStyleSheet("background-color: #E6E6FA;")
                self.analyze_financial_button.setStyleSheet("background-color: #E6E6FA;")
            except Exception as e:
                self.result_display.append(f"<p style='color: red;'>Erro ao processar o arquivo: {str(e)}</p>")

    def analyze_cost(self):
        """Análise de custos - somente executada se houver arquivo carregado."""
        if self.file_data:
            resposta_gpt = self.cateline_lacet_gpt.get_financial_analysis_response(self.file_data)
            self.result_display.append(f"<p style='color: cyan;'>Resultado da Análise de Custos:\n{resposta_gpt}</p>")
        else:
            self.result_display.append(f"<p style='color: red;'>Por favor, envie um arquivo para realizar a análise de custos.</p>")

    def analyze_financial(self):
        """Análise financeira - somente executada se houver arquivo carregado."""
        if self.file_data:
            resposta_gpt = self.cateline_lacet_gpt.get_financial_analysis_response(self.file_data)
            self.result_display.append(f"<p style='color: cyan;'>Resultado da Análise Financeira:\n{resposta_gpt}</p>")
        else:
            self.result_display.append(f"<p style='color: red;'>Por favor, envie um arquivo para realizar a análise financeira.</p>")

    def cycle_humor(self):
        """Troca o humor e atualiza o ícone e a mensagem de boas-vindas."""
        self.humor_index = (self.humor_index + 1) % len(self.humores)
        humor_message = self.get_dynamic_welcome_message()
        self.result_display.append(f"<p style='color: yellow;'>Catelina Lacet: {humor_message}</p>")
        self.humor_button.setIcon(self.get_humor_icon())

    def get_dynamic_welcome_message(self):
        """Retorna uma mensagem de boas-vindas dinâmica com base no humor atual."""
        humor = self.user_preferences_service.get_humor_atual()
        if humor == 'sarcastico':
            return "Prepare-se para aprender mais sobre finanças... se é que você entende algo disso."
        elif humor == 'compreensivo':
            return "Vamos juntos conquistar sua estabilidade financeira com calma e paciência."
        else:
            return "Vamos começar a jornada para dominar suas finanças!"

    def get_humor_icon(self):
        """Retorna o ícone correspondente ao humor atual."""
        humor = self.humores[self.humor_index]
        if humor == 'sarcastico':
            return QIcon(qtawesome.icon('fa.frown-o', color='red'))
        elif humor == 'compreensivo':
            return QIcon(qtawesome.icon('fa.smile-o', color='green'))
        else:
            return QIcon(qtawesome.icon('fa.smile-o', color='yellow'))
