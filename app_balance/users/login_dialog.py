from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class LoginDialog(QDialog):
    """
    Janela de login para autenticar o usuário existente.
    """
    def __init__(self, user_service):
        super().__init__()
        self.user_service = user_service
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 400, 250)
        self.setup_ui()

        # Aplicando o estilo
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Nome do usuário
        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit()

        # Campo de senha do usuário
        self.password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Oculta a senha durante a digitação

        # Botão de login
        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.fazer_login)

        # Botão para ir para a tela de criar usuário
        self.create_user_button = QPushButton("Criar Conta")
        self.create_user_button.clicked.connect(self.ir_para_criar_usuario)

        # Adicionar widgets ao layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.create_user_button)

        self.setLayout(layout)

    def apply_styles(self):
        """Aplica o estilo da paleta de cores."""
        self.setStyleSheet("""
            QDialog {
                background-color: #1F1D36;
                font-family: 'Arial', sans-serif;
                font-size: 16px;
                color: #E94560;
            }

            QLabel {
                color: #E94560;
            }

            QLineEdit {
                background-color: #FFE3E3;
                color: #2C003E;
                border: 2px solid #2C003E;
                border-radius: 8px;
                padding: 5px;
            }

            QPushButton {
                background-color: #6A0572;
                color: #F9F3F3;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #890F76;
            }
        """)

    def fazer_login(self):
        nome = self.name_input.text()
        senha = self.password_input.text()

        # Validação do login aqui (adicionar a lógica correta para autenticação)
        usuario = self.user_service.carregar_usuario_existente(nome)
        if usuario:
            # Verifica a senha aqui, por exemplo usando bcrypt
            # Se a senha estiver correta, aceita o diálogo de login
            self.accept()  # Fecha o diálogo se o login for bem-sucedido
        else:
            # Se falhar no login, limpa os campos e mostra uma mensagem
            self.name_input.clear()
            self.password_input.clear()
            self.name_input.setPlaceholderText("Erro! Tente novamente.")

    def ir_para_criar_usuario(self):
        """
        Fecha o diálogo de login e abre o diálogo de criação de usuário.
        """
        self.reject()  # Fecha o diálogo de login para abrir o de criação
