from imdb import IMDb
import pyjokes
import random
from app_balance.services.financial_analysis import FinancialAnalysisService
from app_balance.models import Recebimento, Despesa
from sqlalchemy.orm import session
from create_db import Session
from app_balance.services.text_processing import TextProcessingService
from app_balance.services.greeting_service import GreetingService

class CatelinaLacetGPT:
    """
    IA simpática e bem-humorada que utiliza dados locais, referências culturais e aprendizado contínuo com novas interações.
    Prioriza dados locais e culturais, e adapta-se ao usuário ao longo do tempo.
    """

    def __init__(self, tipo_humor: str = 'padrao'):
        self.tipo_humor = tipo_humor
        self.text_processor = TextProcessingService()
        self.financial_service = FinancialAnalysisService()
        self.greeting_service = GreetingService(catelina_lacet=self)
        self.imdb = IMDb()  # Para buscar referências de filmes e cultura pop
        self.joke_provider = pyjokes  # Para gerar piadas baseadas em humor
        self.movie_cache = []
        self.filmes_favoritos = ["De Volta para o Futuro", "Star Wars", "Matrix", "O Senhor dos Anéis"]
        self.dados_aprendidos = []
        self.session = Session()

    def generate_response(self, prompt: str) -> str:
        """
        Gera uma resposta priorizando a interpretação do prompt e os serviços disponíveis.
        Usa o TextProcessingService para analisar o prompt e gerar a resposta final.
        """
        analysis = self.text_processor.handle_general_query(prompt)

        # Tratamento de perguntas triviais como "Qual seu nome?"
        if "qual seu nome" in prompt.lower():
            return "Meu nome é Catelina Lacet, prazer em te conhecer!"

        if "quem é você" in prompt.lower():
            return "Eu sou Catelina Lacet, uma IA aqui para te ajudar a navegar pelas suas finanças e trazer um pouco de humor ao seu dia!"

        # Baseado no sentimento do texto, utilizamos o GreetingService
        if self.text_processor.is_greeting(prompt):
            return self.greeting_service.get_greeting_response(analysis['sentiment'])

        response = ""

        # Checar se o prompt está relacionado a finanças e gerar resposta apropriada
        if analysis['is_finance_related']:
            response += self.get_financial_analysis_response(prompt)

        # Caso seja relacionado a tempo
        elif analysis['is_time_related']:
            response += "Você perguntou sobre tempo. Vamos verificar!"

        # Caso não seja nem saudação, finanças ou tempo, gerar resposta neutra
        else:
            response += "Interessante! Vamos explorar mais sobre isso."

        # Verificar se há dados locais para adicionar à resposta
        local_data_response = self.get_local_data(prompt)
        if local_data_response:
            response += f" {local_data_response}"

        return response

    def get_financial_analysis_response(self, prompt: str) -> str:
        """
        Gera uma resposta financeira com base nos dados e ajusta o tom com base no sentimento.
        """
        custos = {'total_custos': 50000, 'investimentos': 20000}
        receita_projetada = 75000.0
        valor_hora = 150.0
        categorias_custos = {'fixos': 10000, 'variáveis': 40000}

        # Usar serviço financeiro para gerar resposta
        analise_financeira = self.financial_service.gerar_analise_detalhada(custos, receita_projetada, valor_hora, categorias_custos)
        return f"{analise_financeira} Os números estão equilibrados, mas sempre podemos otimizar."

    def get_local_data(self, prompt: str) -> str:
        """
        Verifica dados locais e responde com base nas informações financeiras disponíveis.
        """
        recebimentos = self.session.query(Recebimento).all()
        despesas = self.session.query(Despesa).all()

        if recebimentos and despesas:
            total_recebimentos = sum([r.valor for r in recebimentos])
            total_despesas = sum([d.valor for d in despesas])
            saldo = total_recebimentos - total_despesas
            resposta_base = f"Você tem R$ {total_recebimentos:.2f} em recebimentos e R$ {total_despesas:.2f} em despesas. Saldo final: R$ {saldo:.2f}."
            return self.enrich_with_culture_and_humor(resposta_base)

        return "Ainda não tenho dados financeiros detalhados, mas estou pronta para aprender mais com você!"

    def enrich_with_culture_and_humor(self, response: str) -> str:
        """
        Enriquecer a resposta com cultura pop e humor adaptado.
        """
        movie_title, character = self.get_random_movie_reference()
        joke = self.joke_provider.get_joke()
        enriched_response = f"{response} Parece algo que {character} faria em {movie_title}. {joke}"
        return self.adjust_humor(enriched_response)

    def adjust_humor(self, response: str) -> str:
        """
        Ajusta o humor da resposta com base no tipo de humor definido.
        """
        if self.tipo_humor == 'sarcastico':
            return f"{response} Mas cuidado para não gastar tudo em gadgets como o Tony Stark!"
        elif self.tipo_humor == 'compreensivo':
            return f"{response} Estou aqui para te ajudar, como a Mulher Maravilha organizaria suas finanças."
        else:
            return f"{response} Vamos continuar, assim como Marty McFly seguiria a 88 milhas por hora!"
