import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter  # Adiciona essa linha para corrigir o antialiasing
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA

# Adiciona o diretório raiz ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_balance.prompts import PromptService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App de Análise de Custos")
        self.setGeometry(100, 100, 1000, 800)

        # Inicializar o serviço de prompts
        self.prompt_service = PromptService()

        # Layout principal
        layout = QVBoxLayout()

        # Rótulo de boas-vindas
        self.label = QLabel("Bem-vindo ao App de Análise de Custos")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Botão para enviar arquivos (Excel, PDF, DOCX)
        self.upload_button = QPushButton("Enviar Arquivos")
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        # Campo de resultados
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        # Botão para exibir gráficos
        self.chart_button = QPushButton("Exibir Gráficos Financeiros")
        self.chart_button.clicked.connect(self.show_graphs)
        layout.addWidget(self.chart_button)

        # Configura o widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

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
                    self.result_label.setText(result)
                except Exception as e:
                    self.result_label.setText(f"Erro ao processar o arquivo {file}: {str(e)}")

    def show_graphs(self):
        """Exibe gráficos com base nos dados financeiros gerados."""
        try:
            # Simulação de dados de receitas e custos para exibir gráficos
            custos = 10000  # Valor simulado de custos
            receita = 15000  # Valor simulado de receita

            # Exibe gráficos de receitas e despesas
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

            # Corrigindo o antialiasing com QPainter
            chart_view.setRenderHint(QPainter.Antialiasing)

            chart_widget = QWidget()
            chart_layout = QVBoxLayout()
            chart_layout.addWidget(chart_view)
            chart_widget.setLayout(chart_layout)
            chart_widget.setWindowTitle("Distribuição de Custos")
            chart_widget.show()

            meses = np.arange(1, 13)
            receitas = receita + np.random.uniform(-0.1, 0.1, 12) * receita

            plt.figure(figsize=(10, 6))
            sns.lineplot(x=meses, y=receitas, marker="o")
            plt.title("Evolução da Receita nos Próximos 12 Meses")
            plt.xlabel("Meses")
            plt.ylabel("Receita Estimada (R$)")
            plt.grid(True)
            plt.show()

            slope, intercept, r_value, p_value, std_err = stats.linregress(meses, receitas)
            regression_message = f"Análise de tendência: Inclinação = {slope:.2f}, P-valor = {p_value:.4f}"
            self.result_label.setText(regression_message)

            # Previsão de receita usando ARIMA
            model = ARIMA(receitas, order=(1, 1, 1))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=12)

            plt.figure(figsize=(10, 6))
            plt.plot(meses, receitas, label="Receita Observada")
            plt.plot(np.arange(13, 25), forecast, label="Previsão com ARIMA", linestyle="--")
            plt.title("Previsão de Receita com ARIMA")
            plt.xlabel("Meses")
            plt.ylabel("Receita Estimada (R$)")
            plt.legend()
            plt.grid(True)
            plt.show()

            data = pd.DataFrame({
                'Meses': np.concatenate([meses, np.arange(13, 25)]),
                'Receita': np.concatenate([receitas, forecast])
            })

            fig = px.line(data, x='Meses', y='Receita', title="Previsão de Receita com ARIMA (Plotly)")
            fig.show()

        except ValueError:
            self.result_label.setText("Por favor, insira valores válidos para os gráficos.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
