from app_balance.services.text_processing import TextProcessingService
from app_balance.services.greeting_service import GreetingService
from app_balance.services.financial_analysis import FinancialAnalysisService
from app_balance.services.file_processing_service import FileProcessingService
from app_balance.services.advanced_financial_analysis import AdvancedFinancialAnalysisService
import random
from imdb import IMDb
import pyjokes

class CatelinaLacetGPT:
    """
    IA simpática e bem-humorada que utiliza dados locais, referências culturais, humor e aprendizado contínuo com novas interações.
    Especialista em finanças, mas flexível para interpretar e responder a qualquer tópico de forma natural.
    """

    def __init__(self, tipo_humor: str = 'padrao'):
        self.tipo_humor = tipo_humor
        self.text_processor = TextProcessingService()
        self.financial_service = FinancialAnalysisService()
        self.file_service = FileProcessingService()
        self.advanced_financial_service = AdvancedFinancialAnalysisService()
        self.greeting_service = GreetingService(catelina_lacet=self)
        self.imdb = IMDb()  # Para buscar referências de filmes e cultura pop
        self.joke_provider = pyjokes  # Para gerar piadas baseadas em humor
        self.movie_cache = []
        self.filmes_favoritos = ["De Volta para o Futuro", "Star Wars", "Matrix", "O Senhor dos Anéis"]

    def generate_response(self, prompt: str, file_data=None, horas_trabalhadas=None) -> str:
        """
        Usa o processamento do TextProcessingService para interpretar o texto do prompt de forma natural
        e toma decisões sobre como gerar uma resposta apropriada.
        """
        # Processamos o prompt com o serviço de processamento de texto
        analysis = self.text_processor.process_prompt(prompt)

        # Se for uma saudação
        if self.text_processor.is_greeting(prompt):
            return self.greeting_service.get_greeting_response(analysis['sentiment'])

        # Se for relacionado a finanças
        if self.is_financial_prompt(analysis['keywords'], prompt):
            if file_data and horas_trabalhadas:
                return self.get_financial_analysis_response(file_data, horas_trabalhadas)
            else:
                return "Por favor, envie um arquivo financeiro e informe as horas trabalhadas para que eu possa calcular."

        # Se o prompt não for finanças ou saudação, responder com transformers
        return self.text_processor.answer_with_transformers(prompt)

    def is_financial_prompt(self, keywords: list, prompt: str) -> bool:
        """
        Verifica se as palavras-chave do prompt estão relacionadas a finanças.
        """
        financial_keywords = ['finança', 'dinheiro', 'investimento', 'gastos', 'despesa', 'imposto', 'taxa', 'juros', 'renda', 'conta', 'lucro', 'ROI', 'ponto de equilíbrio']
        return any(keyword in financial_keywords for keyword in keywords) or any(term in prompt.lower() for term in financial_keywords)

    def get_financial_analysis_response(self, file_data, horas_trabalhadas: float) -> str:
        """
        Processa o arquivo enviado para extrair dados financeiros reais e gerar uma análise detalhada com base nas horas trabalhadas.
        """
        try:
            financial_data = self.file_service.processar_arquivo(file_data, "excel")
            custos = {'total_custos': financial_data['total_custos'], 'investimentos': financial_data.get('investimentos', 0)}
            receita_projetada = financial_data['receita_projetada']
            categorias_custos = financial_data['categorias_custos']

            # Gerar análise usando os dados reais extraídos e as horas trabalhadas dinâmicas
            analise_financeira = self.financial_service.gerar_analise_detalhada(custos, receita_projetada, horas_trabalhadas, categorias_custos)
            return analise_financeira
        except Exception as e:
            return f"Erro ao processar o arquivo: {str(e)}"
