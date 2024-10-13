# app_balance/services/gpt_module.py
import openai
from environs import Env
from typing import Dict
from .financial_analysis import FinancialAnalysisService

# Carregar variáveis de ambiente para a chave da API do OpenAI
env = Env()
env.read_env()

# Definir a chave da API do OpenAI
openai.api_key = env.str("OPENAI_API_KEY")


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
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Houve um erro ao se comunicar com o GPT-4: {str(e)}"

    def generate_dynamic_references(self) -> str:
        """
        Gera uma resposta GPT-4 que inclui citações e referências aleatórias sobre filmes,
        heróis e cultura pop, com foco em finanças e negócios.

        Returns:
            str: Uma resposta gerada dinamicamente usando o GPT-4.
        """
        prompt = """
        Crie uma análise engraçada e criativa com referências a filmes dos anos 80, 90 e 2000,
        super-heróis, e cultura pop para contextualizar uma análise financeira. Misture humor
        e sabedoria prática para tornar o assunto mais leve e divertido.
        """
        return self.generate_gpt_response(prompt)

    def get_financial_analysis(self, custos: Dict, receita_projetada: float, valor_hora: float, categorias_custos: Dict) -> str:
        """
        Realiza a análise financeira e usa o GPT-4 para adicionar insights criativos e divertidos.

        Args:
            custos (dict): Dados financeiros sobre custos.
            receita_projetada (float): Receita projetada.
            valor_hora (float): Valor da hora trabalhada.
            categorias_custos (dict): Categorias detalhadas de custos.

        Returns:
            str: A análise enriquecida com a personalidade da Catelina Lacet.
        """
        # Realiza a análise financeira com base nos cálculos do FinancialAnalysisService
        analysis = self.financial_service.gerar_analise_detalhada(custos, receita_projetada, valor_hora, categorias_custos)

        # Cria o prompt para o GPT-4 adicionar insights criativos baseados na análise financeira
        prompt = f"Aqui está uma análise financeira: {analysis}. Por favor, adicione uma visão divertida e útil com referências de cultura pop e filmes."

        # Gera resposta usando GPT-4
        gpt_response = self.generate_gpt_response(prompt)

        # Combina a resposta da análise financeira com humor e citações dinâmicas
        dynamic_references = self.generate_dynamic_references()

        return f"{gpt_response}\n\nAlém disso, Catelina Lacet diz: {dynamic_references}"
