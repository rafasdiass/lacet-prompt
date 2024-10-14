from transformers import pipeline
import random
from app_balance.services.text_processing import TextProcessingService
from app_balance.services.greeting_service import GreetingService
from app_balance.services.financial_analysis import FinancialAnalysisService
from app_balance.services.file_processing_service import FileProcessingService
from app_balance.services.advanced_financial_analysis import AdvancedFinancialAnalysisService
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
        # Usando transformers para responder perguntas gerais e interpretar qualquer tópico
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

    def generate_response(self, prompt: str, file_data=None) -> str:
        """
        Usa o processamento do TextProcessingService para interpretar o texto do prompt de forma natural
        e toma decisões sobre como gerar uma resposta apropriada, sem depender de palavras-chave específicas.
        """
        analysis = self.text_processor.process_prompt(prompt)  # Processamento do texto

        # Se o prompt for uma saudação
        if self.text_processor.is_greeting(prompt):
            return self.greeting_service.get_greeting_response(analysis['sentiment'])

        # Se for relacionado a finanças, redirecionar para o serviço correto
        if any(keyword in ['finança', 'dinheiro', 'investimento', 'gastos', 'despesa', 'imposto', 'taxa', 'juros'] for keyword in analysis['keywords']):
            if file_data:
                return self.get_financial_analysis_response(file_data)
            else:
                return "Por favor, envie um documento financeiro para análise."

        # Perguntas complexas ou tópicos fora de finanças e cultura pop, usar transformers
        return self.answer_general_question(prompt)

    def get_financial_analysis_response(self, file_data) -> str:
        """
        Processa o arquivo enviado para extrair dados financeiros reais e gerar uma análise detalhada.
        """
        try:
            # Processar o arquivo e extrair os dados
            financial_data = self.file_service.processar_arquivo(file_data, "excel")

            # Extrair as informações necessárias para a análise
            custos = {'total_custos': financial_data['total_custos'], 'investimentos': financial_data.get('investimentos', 0)}
            receita_projetada = financial_data['receita_projetada']
            valor_hora = 150.0  # Pode ser parametrizado se necessário
            categorias_custos = financial_data['categorias_custos']

            # Gerar análise usando os dados reais extraídos
            analise_financeira = self.financial_service.gerar_analise_detalhada(custos, receita_projetada, valor_hora, categorias_custos)
            return analise_financeira
        except Exception as e:
            return f"Erro ao processar o arquivo: {str(e)}"

    def answer_general_question(self, prompt: str) -> str:
        """
        Usa o modelo de transformers para responder a qualquer tipo de pergunta ou tópico.
        """
        context = """
        Sou uma IA com vasto conhecimento em finanças, cultura pop, ciência e muito mais. 
        Posso te ajudar com temas variados, desde orçamento pessoal até curiosidades sobre filmes e séries.
        """
        result = self.qa_pipeline(question=prompt, context=context)
        return result['answer']
