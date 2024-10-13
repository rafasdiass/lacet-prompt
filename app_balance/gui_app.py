import os
import sys
import numpy as np  # Usado para cálculos matemáticos
import pandas as pd  # Usado para processar arquivos Excel
import matplotlib.pyplot as plt  # Para exibir gráficos de receitas
import qtawesome  # Para ícones no aplicativo
import seaborn as sns  # Para exibir gráficos de receitas
import plotly.express as px  # Alternativa para gráficos interativos
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog,
    QWidget, QMessageBox, QLineEdit, QTextEdit, QComboBox, QDialog, QHBoxLayout
)
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap, QIcon
from environs import Env  # Para carregar a chave do OpenAI a partir do .env
from datetime import datetime
from typing import Dict

# Imports relativos dentro do pacote
from .prompts import PromptService
from .services.openai_service import analyze_data
from .database import session
from .models import Prompt
from .services.gpt_module import CatelinaLacetGPT

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catelina Lacet - Sua IA Financeira com Senso de Humor!")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("""
            background-color: #000000;  /* Fundo preto */
            color: #EDEDED;  /* Texto claro */
        """)

        self.prompt_service = PromptService()
        self.catelina_gpt = CatelinaLacetGPT()  # Inicializa com humor padrão

        # Inicializa as variáveis de dados reais
        self.real_cost_data = None
        self.real_revenue_data = None

        # Layout principal
        layout = QVBoxLayout()

        # Logo
        self.logo = QLabel()
        pixmap = QPixmap('assets/LOGO-BRANCA.PNG')
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setFixedSize(200, 100)
        self.logo.setScaledContents(True)
        layout.addWidget(self.logo)

        # Botão de engrenagem para mudar humor
        self.humor_button = QPushButton(" Humor")
        self.humor_button.setIcon(qtawesome.icon('fa.cog', color='black'))
        self.humor_button.setStyleSheet("""
            background-color: #F8F4E3;
            color: black;
            font-size: 16px;
            padding: 10px;
        """)
        self.humor_button.clicked.connect(self.abrir_mudanca_humor_dialogo)
        layout.addWidget(self.humor_button)

        # Mensagem de boas-vindas dinâmica, gerada pela Catelina Lacet
        self.label = QLabel(self.catelina_gpt.generate_dynamic_references())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #F8F4E3;
        """)
        layout.addWidget(self.label)

        # Botões
        self.analyze_cost_button = QPushButton(" Análise de Custos")
        self.analyze_cost_button.setIcon(qtawesome.icon('fa.money', color='black'))
        self.analyze_cost_button.setStyleSheet("""
            background-color: #F8F4E3;
            color: black;
            font-size: 16px;
            padding: 10px;
        """)
        self.analyze_cost_button.clicked.connect(self.analyze_cost_prompt)
        layout.addWidget(self.analyze_cost_button)

        self.analyze_investment_button = QPushButton(" Análise de Investimentos")
        self.analyze_investment_button.setIcon(qtawesome.icon('fa.line-chart', color='black'))
        self.analyze_investment_button.setStyleSheet("""
            background-color: #F8F4E3;
            color: black;
            font-size: 16px;
            padding: 10px;
        """)
        self.analyze_investment_button.clicked.connect(self.analyze_investment_prompt)
        layout.addWidget(self.analyze_investment_button)

        # Botão de Upload de Arquivos
        self.upload_button = QPushButton(" Enviar Arquivos")
        self.upload_button.setIcon(qtawesome.icon('fa.upload', color='black'))
        self.upload_button.setStyleSheet("""
            background-color: #F8F4E3;
            color: black;
            font-size: 16px;
            padding: 10px;
        """)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        # Campo de input para comunicação com o GPT-4
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Digite sua pergunta para a Catelina Lacet...")
        self.input_field.setStyleSheet("padding: 10px; font-size: 16px;")
        layout.addWidget(self.input_field)

        # Botão para enviar input para o GPT-4
        self.gpt_button = QPushButton("Enviar Pergunta para Catelina Lacet")
        self.gpt_button.setStyleSheet("""
            background-color: #F8F4E3;
            color: black;
            font-size: 16px;
            padding: 10px;
        """)
        self.gpt_button.clicked.connect(self.enviar_gpt)
        layout.addWidget(self.gpt_button)

        # Campo de exibição dos resultados
        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("padding: 10px; font-size: 14px;")
        layout.addWidget(self.result_display)

        # Configura o widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def abrir_mudanca_humor_dialogo(self):
        """
        Abre um diálogo para o usuário escolher o tipo de humor da IA.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Escolher Humor")
        dialog.setGeometry(300, 300, 300, 150)

        dialog_layout = QVBoxLayout()

        humor_selector = QComboBox(dialog)
        humor_selector.addItems(['Padrão', 'Sarcastico', 'Compreensivo'])
        humor_selector.setStyleSheet("font-size: 16px; padding: 10px;")
        humor_selector.currentIndexChanged.connect(lambda: self.set_humor_type(humor_selector.currentText()))
        dialog_layout.addWidget(humor_selector)

        confirmar_button = QPushButton("Confirmar", dialog)
        confirmar_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(confirmar_button)

        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def set_humor_type(self, tipo_humor: str):
        """
        Define o tipo de humor com base na escolha do usuário no ComboBox.
        """
        tipo_humor = tipo_humor.lower()
        if tipo_humor == 'sarcastico':
            self.catelina_gpt.definir_tipo_humor('sarcastico')
        elif tipo_humor == 'compreensivo':
            self.catelina_gpt.definir_tipo_humor('compreensivo')
        else:
            self.catelina_gpt.definir_tipo_humor('padrao')

    def analyze_cost_prompt(self):
        # Catelina Lacet interage com humor para iniciar a análise de custos
        response = self.catelina_gpt.get_financial_analysis(
            custos={'total_custos': 10000},
            receita_projetada=15000,
            valor_hora=120.0,
            categorias_custos={'Serviços': 4000, 'Infraestrutura': 2000, 'Funcionários': 4000}
        )
        self.result_display.setText(response)
        QMessageBox.information(self, "Análise de Custos", response)

    def analyze_investment_prompt(self):
        # Catelina Lacet traz insights bem-humorados para análise de investimentos
        response = self.catelina_gpt.generate_dynamic_references()
        self.result_display.setText(response)
        QMessageBox.information(self, "Análise de Investimentos", response)

    def upload_file(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Enviar Arquivos",
            os.getenv('HOME'),
            "All Files (*);;Excel Files (*.xlsx);;CSV Files (*.csv)",
            options=options
        )
        if files:
            for file in files:
                file_type = file.split('.')[-1].lower()
                try:
                    # Processar o arquivo
                    result = self.prompt_service.processar_arquivo(file, file_type)

                    # Obter dados reais dos custos e receitas a partir do arquivo
                    self.real_cost_data = result['total_custos']
                    self.real_revenue_data = result['receita_projetada']

                    prompt = self.prompt_service.gerar_prompt_analise(
                        custos={'total_custos': self.real_cost_data},
                        valor_hora=120.0,
                        categorias_custos=result['categorias_custos'],
                        margem_lucro_desejada=20.0,
                        receita_projetada=self.real_revenue_data
                    )

                    # Obter análise prioritária do GPT-4
                    response = analyze_data(prompt)
                    self.result_display.setText(response)

                    # Exibir gráficos como suporte à análise do GPT-4
                    self.show_graphs()

                except Exception as e:
                    self.result_display.setText(f"Erro ao processar o arquivo {file}: {str(e)}")

    def enviar_gpt(self):
        """Envia uma pergunta diretamente ao GPT-4 e salva no banco de dados."""
        prompt_text = self.input_field.text()

        if prompt_text:
            try:
                # Salvar o prompt no banco de dados
                novo_prompt = Prompt(conteudo=prompt_text, data=datetime.now())
                session.add(novo_prompt)
                session.commit()

                # Enviar ao GPT-4
                resposta_gpt = analyze_data(prompt_text)
                self.result_display.setText(resposta_gpt)

                # Salvar a resposta do GPT-4 no banco de dados
                novo_prompt.resposta = resposta_gpt
                session.commit()

            except Exception as e:
                self.result_display.setText(f"Erro ao enviar pergunta ao GPT-4: {str(e)}")
        else:
            self.result_display.setText("Por favor, insira uma pergunta válida.")

    def show_graphs(self):
        """Exibe gráficos com base nos dados financeiros, sejam simulados ou reais."""
        try:
            custos = self.real_cost_data if self.real_cost_data else 10000
            receita = self.real_revenue_data if self.real_revenue_data else 15000

            # Gráfico de Distribuição de Custos
            categorias_custos = ["Serviços", "Infraestrutura", "Funcionários"]
            valores_custos = [custos * 0.4, custos * 0.2, custos * 0.4]

            series = QPieSeries()
            series.append("Serviços", valores_custos[0])
            series.append("Infraestrutura", valores_custos[1])
            series.append("Funcionários", valores_custos[2])

            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("Distribuição de Custos")

            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.Antialiasing)

            chart_widget = QWidget()
            chart_layout = QVBoxLayout()
            chart_layout.addWidget(chart_view)
            chart_widget.setLayout(chart_layout)
            chart_widget.setWindowTitle("Distribuição de Custos")
            chart_widget.show()

            # Gráfico de Evolução da Receita
            meses = np.arange(1, 13)
            receitas = receita + np.random.uniform(-0.1, 0.1, 12) * receita

            plt.figure(figsize=(10, 6))
            sns.lineplot(x=meses, y=receitas, marker="o")
            plt.title("Evolução da Receita nos Próximos 12 Meses")
            plt.xlabel("Meses")
            plt.ylabel("Receita Estimada (R$)")
            plt.grid(True)
            plt.show()

        except ValueError:
            self.result_display.setText("Por favor, insira valores válidos para os gráficos.")
