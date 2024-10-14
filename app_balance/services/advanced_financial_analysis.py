import pandas as pd
import pandas_datareader as pdr
import numpy as np
import datetime
from typing import Dict


class AdvancedFinancialAnalysisService:
    """
    Serviço avançado para realizar análises financeiras com dados de mercado,
    indicadores técnicos, simulações de investimentos e cálculos de valor presente.
    Inclui impostos, taxas e juros compostos.
    """

    def __init__(self, start_date=None, end_date=None):
        # Definir datas de análise (últimos 6 meses por padrão)
        self.start_date = start_date or (
            datetime.datetime.now() - datetime.timedelta(days=180)
        )
        self.end_date = end_date or datetime.datetime.now()

    def get_market_data(self, ticker: str) -> pd.DataFrame:
        """
        Busca dados de mercado para o ticker especificado usando Yahoo Finance.
        Args:
            ticker (str): Código da ação (exemplo: 'AAPL' para Apple).
        Returns:
            pd.DataFrame: DataFrame com os dados de mercado (preços diários).
        """
        try:
            market_data = pdr.get_data_yahoo(ticker, self.start_date, self.end_date)
            return market_data
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar dados de mercado: {str(e)}")

    def calculate_technical_indicators(self, market_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula indicadores técnicos com base nos dados de mercado usando pandas.
        Args:
            market_data (pd.DataFrame): Dados de mercado com preços diários.
        Returns:
            pd.DataFrame: DataFrame com os indicadores técnicos adicionados.
        """
        # Calculando média móvel simples (SMA) de 50 dias
        market_data["SMA_50"] = market_data["Close"].rolling(window=50).mean()

        # Calculando o Índice de Força Relativa (RSI)
        delta = market_data["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        market_data["RSI"] = 100 - (100 / (1 + rs))

        # Calculando o MACD (diferença entre a média móvel de 12 e 26 dias)
        market_data["EMA_12"] = market_data["Close"].ewm(span=12, adjust=False).mean()
        market_data["EMA_26"] = market_data["Close"].ewm(span=26, adjust=False).mean()
        market_data["MACD"] = market_data["EMA_12"] - market_data["EMA_26"]
        market_data["MACD_signal"] = (
            market_data["MACD"].ewm(span=9, adjust=False).mean()
        )

        return market_data

    def simulate_investment(
        self,
        initial_investment: float,
        market_data: pd.DataFrame,
        taxa_imposto: float = 0.15,
    ) -> float:
        """
        Simula um investimento com base nos dados históricos de mercado, aplicando imposto.
        Args:
            initial_investment (float): Valor inicial do investimento.
            market_data (pd.DataFrame): Dados de mercado com preços diários.
            taxa_imposto (float): Percentual de imposto aplicado sobre o ganho de capital.
        Returns:
            float: Valor final do investimento após o período com impostos aplicados.
        """
        # Preço inicial e final para cálculo do retorno
        start_price = market_data["Close"].iloc[0]
        end_price = market_data["Close"].iloc[-1]

        # Calcula o retorno do investimento
        investment_return = (end_price - start_price) / start_price
        ganho_bruto = initial_investment * (1 + investment_return)

        # Calcula o imposto sobre o ganho de capital
        imposto = (ganho_bruto - initial_investment) * taxa_imposto

        # Valor final após imposto
        final_value = ganho_bruto - imposto

        return final_value
