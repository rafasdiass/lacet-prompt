from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox

class UserCreationDialog(QDialog):
    """
    Janela modal para criar um usuário com seleção de humor e idioma por menus suspensos.
    Estilo com paleta de cores de Inverno Brilhante, com contraste e toques femininos.
    """
    def __init__(self, user_service):
        super().__init__()
        self.user_service = user_service
        self.setWindowTitle("Criar Usuário")
        self.setGeometry(300, 300, 400, 300)
        self.setup_ui()

        # Aplicando o estilo ao diálogo inteiro
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Nome do usuário
        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit()

        # Email do usuário
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()

        # Humor preferido com QComboBox
        self.humor_label = QLabel("Humor Preferido:")
        self.humor_combo = QComboBox()
        self.humor_combo.addItems(["Padrão", "Compreensivo", "Sarcastico"])

        # Idioma preferido com QComboBox
        self.language_label = QLabel("Idioma Preferido:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["pt", "en"])

        # Botão para criar usuário
        self.create_button = QPushButton("Criar Usuário")
        self.create_button.clicked.connect(self.criar_usuario)

        # Adicionar widgets ao layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.humor_label)
        layout.addWidget(self.humor_combo)
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def apply_styles(self):
        """
        Aplica o estilo da paleta de cores Inverno Brilhante na interface.
        """
        # Definindo os estilos para toda a janela
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

            QComboBox {
                background-color: #FFE3E3;
                color: #2C003E;
                border: 2px solid #2C003E;
                border-radius: 8px;
                padding: 5px;
            }

            QComboBox QAbstractItemView {
                selection-background-color: #E94560;
                selection-color: #F9F3F3;
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

    def criar_usuario(self):
        nome = self.name_input.text()
        email = self.email_input.text()
        humor = self.humor_combo.currentText()  # Obtém o texto selecionado no combo box
        idioma = self.language_combo.currentText()  # Obtém o idioma selecionado no combo box

        # Cria o usuário no banco de dados
        usuario = self.user_service.criar_usuario_dinamico(nome, email, humor, idioma)

        if usuario:
            self.accept()  # Fecha o diálogo e retorna o controle para a janela principal
        else:
            self.name_input.clear()
            self.email_input.clear()
            self.name_input.setPlaceholderText("Erro! Tente novamente.")
