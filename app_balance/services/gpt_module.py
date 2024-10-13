from openai import OpenAI
from environs import Env
from typing import Dict
from .financial_analysis import FinancialAnalysisService

# Carregar variáveis de ambiente para a chave da API do OpenAI
env = Env()
env.read_env()

# Definir a chave da API do OpenAI
client = OpenAI(api_key=env.str("OPENAI_API_KEY"))

class CatelinaLacetGPT:
    """
    A simpática e bem-humorada IA 'Catelina Lacet' que usa GPT-4 para fornecer análises
    financeiras com referências divertidas a filmes e heróis.
    """

    def __init__(self):
        self.financial_service = FinancialAnalysisService()

    def generate_gpt_response(self, prompt: str) -> str:
        """
        Gera uma resposta usando GPT-4.

        Args:
            prompt (str): O prompt de entrada para gerar a resposta.

        Returns:
            str: A resposta gerada pelo GPT-4.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Houve um erro ao se comunicar com o GPT-4: {str(e)}"
