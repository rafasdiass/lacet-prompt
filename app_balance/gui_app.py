from dearpygui.dearpygui import *  # Importação correta da biblioteca
from app_balance.services.text_processing import TextProcessingService
from app_balance.processamento.file_processing_service import FileProcessingService
from app_balance.users.user_preferences_service import UserPreferencesService
from app_balance.services.catelina_lacet import CatelinaLacetGPT

<<<<<<< HEAD

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
=======
class MainWindow:
    def __init__(self, usuario):
        self.usuario = usuario

        # Inicializando os serviços
        self.text_processor = TextProcessingService()
        self.file_service = FileProcessingService()
        self.user_preferences_service = UserPreferencesService()
        self.cateline_lacet_gpt = CatelinaLacetGPT()
>>>>>>> main

        # Variáveis para armazenar dados do usuário
        self.file_data = None

        # Estado inicial do humor
        self.humores = ["padrao", "compreensivo", "sarcastico"]
        self.humor_index = 0

        # Inicializando a interface de usuário
        self.setup_ui()

    def setup_ui(self):
        # Definindo a janela principal
        with window(f"Catelina Lacet - Bem-vindo, {self.usuario.nome}!", width=1000, height=800):
            # Layout superior com imagem, botão de humor e logo
            with group(horizontal=True):
                add_image("Cath Image", "assets/img/cath.png", width=80, height=80)

                # Botão para mudar o humor
                add_button("Mudar Humor", callback=self.cycle_humor)
                add_same_line()

<<<<<<< HEAD
        # Imagem cath.png no canto esquerdo
        self.cath_image = QLabel()
        pixmap_cath = QPixmap("assets/img/cath.png")
        self.cath_image.setPixmap(pixmap_cath)
        self.cath_image.setFixedSize(80, 80)
        self.cath_image.setScaledContents(True)
        top_layout.addWidget(self.cath_image, alignment=Qt.AlignLeft)
=======
                # Adiciona o ícone de humor correspondente
                add_image("Humor Icon", self.get_humor_icon(), width=40, height=40)
                add_same_line()
>>>>>>> main

                # Logo da aplicação
                add_image("Logo", "assets/LOGO-BRANCA.PNG", width=120, height=40)

            # Área de texto para exibir as conversas
            add_text(f"Catelina Lacet: {self.get_dynamic_welcome_message()}", color=[233, 69, 96], wrap=800)
            add_separator()

            # Campo de exibição de resultados (listbox atualizado para ser usado com set_value)
            add_listbox("result_display", items=[], height=300, width=900)

            # Campo de entrada de texto
            add_input_text("input_field", hint="Digite sua pergunta para a Catelina Lacet...", width=700)

            # Botão para enviar a pergunta
            add_button("Enviar", callback=self.enviar_pergunta)
            add_same_line()

            # Botão para upload de arquivo
            add_button("Upload de Arquivo", callback=self.upload_file)

    def enviar_pergunta(self, sender, data):
        """
<<<<<<< HEAD
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
=======
        Envia a pergunta para o TextProcessingService e depois recebe a resposta final do Catelina Lacet.
>>>>>>> main
        """
        prompt = get_value("input_field")
        try:
            # Envia o texto para o serviço de processamento de texto
            analysis = self.text_processor.analyze_text(prompt)

            # Exibe a pergunta e o resultado da análise de texto
            result_list = get_value("result_display")
            result_list.append(f"Você: {prompt}")
            set_value("result_display", result_list)

            # Solicita a resposta final da Catelina Lacet
            resposta = self.cateline_lacet_gpt.generate_response(prompt, analysis)

            if resposta:
<<<<<<< HEAD
                self.result_display.append(
                    f"<p style='color: #E94560;'>Catelina Lacet: {resposta}</p>"
                )
                
                # Salva o prompt e a resposta no banco de dados usando o data_service
                self.data_service.save_prompt_and_response(prompt, resposta)

=======
                result_list.append(f"Catelina Lacet: {resposta}")
>>>>>>> main
            else:
                result_list.append("Erro ao processar sua pergunta. Tente novamente mais tarde.")
            
            set_value("result_display", result_list)

        except Exception as e:
            result_list.append(f"Erro: {str(e)}")
            set_value("result_display", result_list)
        set_value("input_field", "")

    def upload_file(self, sender, data):
        """
        Faz o upload do arquivo e envia para o FileProcessingService.
        """
        # Usando o file_dialog para permitir upload de arquivos
        with file_dialog(directory_selector=False, show=True, callback=self.process_file) as dialog_id:
            pass

    def process_file(self, sender, data):
        """
        Processa o arquivo carregado pelo usuário.
        """
        file_path = data[0]
        if file_path:
            try:
                file_type = file_path.split(".")[-1].lower()
                with open(file_path, "rb") as f:
                    self.file_data = f.read()

                # Envia o arquivo para o FileProcessingService
                self.file_service.processar_arquivo(self.file_data, file_type)

                # Exibe a confirmação do upload
                result_list = get_value("result_display")
                result_list.append("Arquivo enviado com sucesso. Processamento em andamento...")
                set_value("result_display", result_list)

            except Exception as e:
                result_list = get_value("result_display")
                result_list.append(f"Erro ao enviar o arquivo: {str(e)}")
                set_value("result_display", result_list)

    def cycle_humor(self, sender, data):
        """Troca o humor e atualiza o ícone e a mensagem de boas-vindas."""
        self.humor_index = (self.humor_index + 1) % len(self.humores)
        humor_message = self.get_dynamic_welcome_message()

        # Atualiza a mensagem e o ícone
        result_list = get_value("result_display")
        result_list.append(f"Catelina Lacet: {humor_message}")
        set_value("result_display", result_list)

        delete_item("Humor Icon")
        add_image("Humor Icon", self.get_humor_icon(), width=40, height=40)

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
        """Retorna o caminho da imagem correspondente ao humor atual."""
        humor = self.humores[self.humor_index]
        if humor == "sarcastico":
            return "assets/icons/frown_red.png"
        elif humor == "compreensivo":
            return "assets/icons/smile_green.png"
        else:
            return "assets/icons/smile_yellow.png"
