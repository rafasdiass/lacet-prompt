# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QMessageBox
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA
import qtawesome as qta  # Para adicionar ícones FontAwesome
from environs import Env  # Para carregar a chave do OpenAI a partir do .env

# Carregar variáveis de ambiente
env = Env()
env.read_env()

# Adicionar o diretório raiz ao sys.path para encontrar os módulos corretamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_balance.prompts import PromptService
from app_balance.services.openai_service import analyze_data  # Integração com OpenAI

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App de Análise de Custos")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("""
            background-color: #000000;  /* Fundo preto */
            color: #EDEDED;  /* Texto claro */
        """)

        # Inicializar o serviço de prompts
        self.prompt_service = PromptService()

        # Dados reais (inicialmente vazios até o envio de arquivos)
        self.real_cost_data = None
        self.real_revenue_data = None

        # Layout principal
        layout = QVBoxLayout()

        # Adicionar logo no topo com tamanho controlado
        self.logo = QLabel()
        pixmap = QPixmap('assets/LOGO-BRANCA.PNG')
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setFixedSize(200, 100)  # Define o tamanho da logo (200x100)
        self.logo.setScaledContents(True)  # Ajusta a imagem ao tamanho especificado sem perder a qualidade
        layout.addWidget(self.logo)

        # Mensagem inicial com opções interativas
        self.label = QLabel("Bem-vinda, Catharina! O que você deseja fazer hoje?")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #F8F4E3;  /* Tom pastel claro */
        """)
        layout.addWidget(self.label)

        # Botões interativos para análise de custos, investimentos, etc.
        self.analyze_cost_button = QPushButton(" Análise de Custos")
        self.analyze_cost_button.setIcon(qta.icon('fa.money', color='black'))  # Ícone de análise de custos
        self.analyze_cost_button.setStyleSheet("""
            background-color: #F8F4E3;  /* Cor bege */
            color: black;
            font-size: 16px;
            padding: 10px;
        """)
        self.analyze_cost_button.setCursor(Qt.PointingHandCursor)
        self.analyze_cost_button.clicked.connect(self.analyze_cost_prompt)
        layout.addWidget(self.analyze_cost_button)

        self.analyze_investment_button = QPushButton(" Análise de Investimentos")
        self.analyze_investment_button.setIcon(qta.icon('fa.line-chart', color='black'))  # Ícone de análise de investimentos
        self.analyze_investment_button.setStyleSheet("""
            background-color: #F8F4E3;  /* Cor bege */
            color: black;
            font-size: 16px;
            padding: 10px;
        """)
        self.analyze_investment_button.setCursor(Qt.PointingHandCursor)
        self.analyze_investment_button.clicked.connect(self.analyze_investment_prompt)
        layout.addWidget(self.analyze_investment_button)

        # Botão para enviar arquivos (Excel, PDF, DOCX) com ícone
        self.upload_button = QPushButton(" Enviar Arquivos")
        self.upload_button.setIcon(qta.icon('fa.upload', color='black'))  # Ícone de upload
        self.upload_button.setStyleSheet("""
            background-color: #F8F4E3;  /* Cor bege */
            color: black;
            font-size: 16px;
            padding: 10px;
        """)
        self.upload_button.setCursor(Qt.PointingHandCursor)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        # Campo de resultados
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        # Configura o widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Chamada para exibir os gráficos automaticamente
        self.show_graphs()

    def analyze_cost_prompt(self):
        """Prompt para iniciar a análise de custos"""
        self.result_label.setText("Vamos começar a análise de custos. Envie um arquivo ou prossiga com os dados atuais.")
        QMessageBox.information(self, "Análise de Custos", "Vamos começar a análise de custos. Envie um arquivo ou prossiga com os dados atuais.")

    def analyze_investment_prompt(self):
        """Prompt para iniciar a análise de investimentos"""
        self.result_label.setText("Vamos iniciar a análise de investimentos. Envie um arquivo ou prossiga com os dados atuais.")
        QMessageBox.information(self, "Análise de Investimentos", "Vamos iniciar a análise de investimentos. Envie um arquivo ou prossiga com os dados atuais.")

    def upload_file(self):
        """Função para enviar arquivos e gerar análise de custos."""
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Enviar Arquivos", "", 
                                                "All Files (*);;Excel Files (*.xlsx);;PDF Files (*.pdf);;DOCX Files (*.docx)", 
                                                options=options)
        if files:
            for file in files:
                file_type = file.split('.')[-1].lower()
                try:
                    with open(file, 'rb') as f:
                        file_content = f.read()
                    result = self.prompt_service.processar_arquivo(file_content, file_type)
                    # Atualizar com dados reais
                    self.result_label.setText(result)

                    # Exemplo: atualiza os dados reais de receita e custos
                    self.real_cost_data = 10000  # Substitua pelo valor real extraído
                    self.real_revenue_data = 15000  # Substitua pelo valor real extraído

                    # Recalcular e exibir gráficos com dados reais
                    self.show_graphs()

                except Exception as e:
                    self.result_label.setText(f"Erro ao processar o arquivo {file}: {str(e)}")

    def show_graphs(self):
        """Exibe gráficos com base nos dados financeiros, sejam simulados ou reais."""
        try:
            # Priorizar dados reais, se existirem; caso contrário, usar valores simulados
            custos = self.real_cost_data if self.real_cost_data else 10000
            receita = self.real_revenue_data if self.real_revenue_data else 15000

            # Exibe gráfico de distribuição de custos usando QChart
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

            # Exibir gráfico de evolução da receita usando Matplotlib e Seaborn
            meses = np.arange(1, 13)
            receitas = receita + np.random.uniform(-0.1, 0.1, 12) * receita

            plt.figure(figsize=(10, 6))
            sns.lineplot(x=meses, y=receitas, marker="o")
            plt.title("Evolução da Receita nos Próximos 12 Meses")
            plt.xlabel("Meses")
            plt.ylabel("Receita Estimada (R$)")
            plt.grid(True)
            plt.show()

            # Chamar automaticamente o GPT-4 para melhorar a análise
            self.analyze_data_with_gpt()

        except ValueError:
            self.result_label.setText("Por favor, insira valores válidos para os gráficos.")

    def analyze_data_with_gpt(self):
        """Função para enviar dados para o GPT-4 e obter insights. Integração automática."""
        if self.real_cost_data and self.real_revenue_data:
            prompt = f"Analisar custos e receita com base nos seguintes dados: Custos = {self.real_cost_data}, Receita = {self.real_revenue_data}."
        else:
            prompt = "Simule uma análise de custos e receita com base em valores padrão de custos (10000) e receita (15000)."

        response = analyze_data(prompt)
        self.result_label.setText(response)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
