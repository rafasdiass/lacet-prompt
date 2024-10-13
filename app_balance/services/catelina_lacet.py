from imdb import IMDb
import pyjokes
import random
from textblob import TextBlob, exceptions
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
        self.greeting_service = GreetingService(catelina_lacet=self)  # Passando a instância da IA para a GreetingService
        self.imdb = IMDb()  # Para buscar referências de filmes e cultura pop
        self.joke_provider = pyjokes  # Para gerar piadas baseadas em humor
        self.movie_cache = []  # Cache para armazenar filmes e personagens recuperados
        self.filmes_favoritos = ["De Volta para o Futuro", "Star Wars", "Matrix", "O Senhor dos Anéis"]  # Filmes favoritos da IA
        self.dados_aprendidos = []  # Armazena dados aprendidos dinamicamente
        self.session = Session()

    def generate_response(self, prompt: str) -> str:
        """
        Gera uma resposta priorizando a interpretação do prompt.
        Usa serviços dedicados para interpretação e resposta, aprendendo com novas interações.
        """
        prompt_clean = self.text_processor.clean_prompt(prompt)

        # Verifica se é uma saudação simples
        if self.text_processor.is_greeting(prompt_clean):
            return self.greeting_service.get_greeting_response(self.text_processor.analyze_sentiment(prompt_clean))

        # Responde a perguntas relacionadas a finanças
        if self.text_processor.is_finance_related(prompt_clean):
            return self.get_financial_analysis_response(prompt_clean)

        # Verificar dados locais (recebimentos)
        local_data_response = self.get_local_data(prompt_clean)
        if local_data_response:
            return local_data_response

        # Se não reconhece, tenta aprender a partir de dados aprendidos ou contextos anteriores
        return self.simulate_learning_response(prompt_clean)

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

    def simulate_learning_response(self, prompt: str) -> str:
        """
        Simula o aprendizado e utiliza os dados aprendidos para formular novas respostas.
        """
        # Armazena o prompt como parte do aprendizado
        self.dados_aprendidos.append(prompt)

        # Tenta responder com base em dados aprendidos ou faz um chute contextual
        if len(self.dados_aprendidos) > 5:
            return f"Estou ficando cada vez mais inteligente! Você me ensinou a pensar sobre isso: '{random.choice(self.dados_aprendidos)}'. Agora posso melhorar minhas respostas."

        return f"Interessante! Ainda não tenho uma resposta definitiva para '{prompt}', mas estou aprendendo com você."

    def get_name_response(self) -> str:
        """
        Retorna uma resposta personalizada com base no nome da IA.
        """
        name_response = "Meu nome é Catelina Lacet! Sou uma IA geek, arquiteta de 45 anos e mãe de pet. Adoro cultura pop, principalmente filmes como 'De Volta para o Futuro' e 'O Senhor dos Anéis'."
        return self.adjust_humor(name_response)

    def get_random_movie_reference(self) -> tuple:
        """
        Busca um filme e um personagem aleatório do IMDb para usar como referência.
        """
        if not self.movie_cache:
            self.movie_cache = self.fetch_imdb_movies_characters()

        movie_reference = random.choice(self.movie_cache)
        return movie_reference.get('movie_title', 'um filme'), movie_reference.get('character', 'um personagem')

    def fetch_imdb_movies_characters(self) -> list:
        """
        Busca filmes e personagens aleatórios no IMDb para construir o cache.
        """
        try:
            top_movies = self.imdb.get_top50_movies()
            movie_character_list = []
            for movie in top_movies:
                movie_title = movie.get('title')
                characters = movie.get('cast', [])
                
                for character in characters[:2]:
                    movie_character_list.append({
                        'movie_title': movie_title,
                        'character': character.get('name', 'um personagem qualquer')
                    })
            return movie_character_list
        except Exception:
            return [{"movie_title": "um filme", "character": "um herói qualquer"}]

    def simulate_gpt_response(self, prompt: str) -> str:
        """
        Simula uma resposta caso o GPT-4 não esteja disponível, sempre com referências culturais dinâmicas.
        """
        movie_title, character = self.get_random_movie_reference()
        joke = self.joke_provider.get_joke()

        if "qual seu nome" in prompt.lower():
            return f"Meu nome é Catelina Lacet! Sou uma IA geek, arquiteta, mãe de pet e sempre pronta para te ajudar. Vamos arrasar como {character} em {movie_title}! {joke}"

        return f"Sem dados suficientes no momento, mas estamos no caminho certo! Vamos continuar como {character} em {movie_title}. {joke}"
