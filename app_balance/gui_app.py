from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QWidget,
    QLineEdit,
    QTextEdit,
    QHBoxLayout,
    QScrollArea,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
import qtawesome
from app_balance.services.text_processing import TextProcessingService
from app_balance.processamento.file_processing_service import FileProcessingService
from app_balance.users.user_preferences_service import UserPreferencesService
from app_balance.services.catelina_lacet import CatelinaLacetGPT


class MainWindow(QMainWindow):
    def __init__(self, usuario, data_service, session):
        super().__init__()
        self.usuario = usuario
        self.data_service = data_service  # Adicionando data_service para persistir dados
        self.setWindowTitle(f"Catelina Lacet - Bem-vindo, {self.usuario.nome}!")
        self.setGeometry(100, 100, 1000, 800)

        # Inicializando os serviços
        self.text_processor = TextProcessingService()  # Serviço para processar texto
        self.file_service = FileProcessingService()  # Serviço para processar arquivos
        self.user_preferences_service = UserPreferencesService(session)  # Passa a sessão aqui
        self.cateline_lacet_gpt = CatelinaLacetGPT()  # IA que devolve a resposta final

        # Variáveis para armazenar dados do usuário
        self.file_data = None

        # Estado inicial do humor
        self.humores = ["padrao", "compreensivo", "sarcastico"]
        self.humor_index = 0

        # Inicializando a interface de usuário
        self.setup_ui()

        # Aplicando a paleta de cores
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Layout para o botão de mudança de humor, logo, e imagem cath.png
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)

        # Imagem cath.png no canto esquerdo
        self.cath_image = QLabel()
        pixmap_cath = QPixmap("assets/img/cath.png")
        self.cath_image.setPixmap(pixmap_cath)
        self.cath_image.setFixedSize(80, 80)
        self.cath_image.setScaledContents(True)
        top_layout.addWidget(self.cath_image, alignment=Qt.AlignLeft)

        # Adiciona um espaço flexível para empurrar os outros widgets para a direita
        top_layout.addStretch()

        # Botão de mudar o humor
        self.humor_button = QPushButton()
        self.humor_button.setIcon(self.get_humor_icon())
        self.humor_button.setIconSize(QSize(40, 40))
        self.humor_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0;
                margin: 0;
            }
        """
        )
        self.humor_button.clicked.connect(self.cycle_humor)

        # Adiciona o botão ao layout, à direita
        top_layout.addWidget(self.humor_button, alignment=Qt.AlignRight)

        # Logo no canto direito
        self.logo = QLabel()
        pixmap_logo = QPixmap("assets/LOGO-BRANCA.PNG")
        self.logo.setPixmap(pixmap_logo)
        self.logo.setFixedSize(120, 40)
        self.logo.setScaledContents(True)

        # Adiciona a logo ao layout, à direita, após o botão
        top_layout.addWidget(self.logo, alignment=Qt.AlignRight)

        # Adiciona o layout superior ao layout principal
        layout.addLayout(top_layout)

        # Área de texto de conversas com rolagem
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet(
            "background-color: #2E2E2E; color: #F9F3F3; font-size: 16px; padding: 10px;"
        )
        scroll_area.setWidget(self.result_display)
        layout.addWidget(scroll_area)

        # Primeira mensagem de boas-vindas da IA
        self.result_display.append(
            f"<p style='color: #E94560;'>Catelina Lacet: {self.get_dynamic_welcome_message()}</p>"
        )

        # Campo de input de texto
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText(
            "Digite sua pergunta para a Catelina Lacet..."
        )
        self.input_field.setStyleSheet(
            "font-size: 16px; padding: 10px; background-color: #FFE3E3; color: #2C003E;"
        )
        self.input_field.setMinimumHeight(60)
        input_layout.addWidget(self.input_field)

        # Botão de enviar pergunta
        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon(qtawesome.icon("fa.paper-plane", color="black")))
        self.send_button.setIconSize(QSize(30, 30))
        self.send_button.setStyleSheet(
            "background-color: #6A0572; border-radius: 8px; color: #F9F3F3;"
        )
        self.send_button.clicked.connect(self.enviar_pergunta)
        input_layout.addWidget(self.send_button)

        # Botão de upload de arquivo
        self.upload_button = QPushButton()
        self.upload_button.setIcon(QIcon(qtawesome.icon("fa.upload", color="black")))
        self.upload_button.setIconSize(QSize(30, 30))
        self.upload_button.setStyleSheet(
            "background-color: #6A0572; border-radius: 8px; color: #F9F3F3;"
        )
        self.upload_button.clicked.connect(self.upload_file)
        input_layout.addWidget(self.upload_button)

        layout.addLayout(input_layout)

        # Definir o widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def apply_styles(self):
        """
        Aplica a paleta de cores Inverno Brilhante para o layout principal da aplicação.
        """
        # Paleta de cores
        background_color = "#1F1D36"  # Fundo roxo escuro
        label_color = "#E94560"  # Texto rosa vibrante
        input_background = "#FFE3E3"  # Campos de input rosa claro
        input_text_color = "#2C003E"  # Texto roxo profundo
        result_background = "#2E2E2E"  # Fundo da área de exibição
        result_text_color = "#F9F3F3"  # Texto claro
        button_background = "#6A0572"  # Botões roxo médio
        button_text_color = "#F9F3F3"  # Texto dos botões branco

        # Aplicar estilo de fundo da janela
        self.setStyleSheet(
            f"""
            background-color: {background_color};
            color: {label_color};
            font-family: 'Arial', sans-serif;
        """
        )

        # Aplicar estilo na área de exibição de resultados
        self.result_display.setStyleSheet(
            f"""
            background-color: {result_background};
            color: {result_text_color};
            border-radius: 8px;
            padding: 10px;
        """
        )

        # Aplicar estilo no campo de entrada
        self.input_field.setStyleSheet(
            f"""
            background-color: {input_background};
            color: {input_text_color};
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
        """
        )

        # Aplicar estilo nos botões
        self.humor_button.setStyleSheet(
            f"""
            background-color: transparent;
            border: none;
        """
        )

        self.send_button.setStyleSheet(
            f"""
            background-color: {button_background};
            color: {button_text_color};
            border-radius: 8px;
            padding: 10px;
        """
        )

        self.upload_button.setStyleSheet(
            f"""
            background-color: {button_background};
            color: {button_text_color};
            border-radius: 8px;
            padding: 10px;
        """
        )

    def enviar_pergunta(self):
        """
        Envia a pergunta para o TextProcessingService, e depois recebe a resposta final do Catelina Lacet.
        """
        prompt = self.input_field.text()
        try:
            # Enviar texto para o TextProcessingService
            analysis = self.text_processor.analyze_text(prompt)

            # Exibe a pergunta e o resultado da análise de texto
            self.result_display.append(f"<p style='color: cyan;'>Você: {prompt}</p>")

            # Solicita a resposta final da Catelina Lacet
            resposta = self.cateline_lacet_gpt.generate_response(prompt, analysis)

            if resposta:
                self.result_display.append(
                    f"<p style='color: #E94560;'>Catelina Lacet: {resposta}</p>"
                )
                
                # Salva o prompt e a resposta no banco de dados usando o data_service
                self.data_service.save_prompt_and_response(prompt, resposta)

            else:
                self.result_display.append(
                    f"<p style='color: red;'>Erro ao processar sua pergunta. Tente novamente mais tarde.</p>"
                )
        except Exception as e:
            self.result_display.append(f"<p style='color: red;'>Erro: {str(e)}</p>")
        self.input_field.clear()

    def upload_file(self):
        """
        Faz o upload do arquivo e envia para o FileProcessingService.
        """
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Selecione um arquivo", "", "Documentos (*.pdf *.xlsx *.docx)"
        )

        if file_path:
            try:
                file_type = file_path.split(".")[-1].lower()
                with open(file_path, "rb") as f:
                    self.file_data = f.read()

                # Enviar o arquivo para o FileProcessingService
                self.file_service.processar_arquivo(self.file_data, file_type)

                # Exibe a confirmação do upload
                self.result_display.append(
                    f"<p style='color: cyan;'>Arquivo enviado com sucesso. Processamento em andamento...</p>"
                )

            except Exception as e:
                self.result_display.append(
                    f"<p style='color: red;'>Erro ao enviar o arquivo: {str(e)}</p>"
                )

    def cycle_humor(self):
        """Troca o humor e atualiza o ícone e a mensagem de boas-vindas."""
        self.humor_index = (self.humor_index + 1) % len(self.humores)
        humor_message = self.get_dynamic_welcome_message()
        self.result_display.append(
            f"<p style='color: #E94560;'>Catelina Lacet: {humor_message}</p>"
        )
        self.humor_button.setIcon(self.get_humor_icon())

    def get_dynamic_welcome_message(self):
        """Retorna uma mensagem de boas-vindas dinâmica com base no humor atual."""
        humor = self.humores[self.humor_index]
        if humor == "sarcastico":
            return "Prepare-se para aprender mais sobre finanças... se é que você entende algo disso."
        elif humor == "compreensivo":
            return "Vamos juntos conquistar sua estabilidade financeira com calma e paciência."
        else:
            return "Vamos começar a jornada para dominar suas finanças!"

    def get_humor_icon(self):
        """Retorna o ícone correspondente ao humor atual."""
        humor = self.humores[self.humor_index]
        if humor == "sarcastico":
            return QIcon(qtawesome.icon("fa.frown-o", color="red"))
        elif humor == "compreensivo":
            return QIcon(qtawesome.icon("fa.smile-o", color="green"))
        else:
            return QIcon(qtawesome.icon("fa.smile-o", color="yellow"))
