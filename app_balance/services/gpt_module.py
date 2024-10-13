from imdb import IMDb
import pyjokes
import random
from app_balance.services.gpt_service import analyze_data
from app_balance.services.financial_analysis import FinancialAnalysisService
from app_balance.models import Recebimento
from sqlalchemy.orm import session

class CatelinaLacetGPT:
    """
    IA simpática e bem-humorada que utiliza dados locais, referências culturais e GPT-4 como complemento.
    A prioridade é sempre os dados locais e referências culturais.
    """

    def __init__(self, tipo_humor: str = 'padrao'):
        self.tipo_humor = tipo_humor
        self.imdb = IMDb()  # Para buscar referências de filmes e cultura pop
        self.joke_provider = pyjokes  # Para gerar piadas baseadas em humor
        self.movie_cache = []  # Cache para armazenar filmes e personagens recuperados
        self.filmes_favoritos = ["De Volta para o Futuro", "Star Wars", "Matrix", "O Senhor dos Anéis"]  # Filmes favoritos da IA
        self.dados_aprendidos = []  # Armazena dados aprendidos dinamicamente
        self.financial_service = FinancialAnalysisService()  # Integração com serviço de análise financeira

    def generate_response(self, prompt: str) -> str:
        """
        Gera uma resposta priorizando dados locais e referências culturais.
        O GPT-4 é utilizado apenas como complemento, se necessário.
        """
        # Responde perguntas sobre filmes favoritos
        if "filme favorito" in prompt.lower():
            return self.get_favorite_movie_response()

        # Gera opinião se perguntado diretamente
        if "opinião" in prompt.lower():
            return self.get_opinion_response()

        # Responde perguntas sobre finanças
        if "análise financeira" in prompt.lower() or "explica finanças" in prompt.lower():
            return self.get_financial_analysis_response(prompt)

        # Prioriza dados locais
        local_data_response = self.get_local_data(prompt)

        if local_data_response:
            return local_data_response

        # Usa GPT-4 como complemento, mas não depende dele
        gpt_response = self.gpt_service.enviar_prompt(prompt)
        if gpt_response:
            return self.enrich_with_culture_and_humor(gpt_response)
        else:
            # Simula resposta fluida se GPT-4 não estiver disponível
            return self.simulate_gpt_response(prompt)

    def get_favorite_movie_response(self) -> str:
        """
        Responde à pergunta sobre o filme favorito da IA.
        """
        movie = random.choice(self.filmes_favoritos)
        return self.adjust_humor(f"Meu filme favorito é {movie}. Sempre me inspiro nele para ajudar nas suas finanças!")

    def get_opinion_response(self) -> str:
        """
        Gera uma resposta genérica de opinião da IA, ajustada ao humor.
        """
        opinions = [
            "Acredito que todos devemos focar em aprender, como o Neo em Matrix. Sempre temos algo novo para dominar.",
            "A força está do seu lado. Assim como em Star Wars, com dedicação, você vai longe!",
            "A melhor coisa que você pode fazer é investir no futuro, como Marty McFly faria!"
        ]
        return self.adjust_humor(random.choice(opinions))

    def get_financial_analysis_response(self, prompt: str) -> str:
        """
        Gera uma análise financeira detalhada com base nos dados fornecidos.
        """
        # Exemplo de dados financeiros fictícios
        custos = {'total_custos': 50000, 'investimentos': 20000}
        receita_projetada = 75000.0
        valor_hora = 150.0
        categorias_custos = {'fixos': 10000, 'variáveis': 40000}

        # Gera o relatório de análise financeira usando o serviço especializado
        analise_financeira = self.financial_service.gerar_analise_detalhada(custos, receita_projetada, valor_hora, categorias_custos)
        return self.adjust_humor(analise_financeira)

    def get_local_data(self, prompt: str) -> str:
        """
        Prioriza dados locais e ajusta conforme o humor e referências culturais.
        """
        if "qual seu nome" in prompt.lower():
            return self.get_name_response()

        # Busca dados financeiros do banco de dados local
        recebimentos = session.query(Recebimento).all()
        if recebimentos:
            total_recebimentos = sum([r.valor for r in recebimentos])
            resposta_base = f"Você tem R$ {total_recebimentos:.2f} em recebimentos! "
            return self.enrich_with_culture_and_humor(resposta_base)

        # Caso não tenha dados financeiros, retorna uma resposta genérica
        return self.enrich_with_culture_and_humor("Ainda não tenho dados financeiros detalhados, mas estou pronta para aprender mais com você!")

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
    
    def get_name_response(self) -> str:
        """
        Retorna uma resposta personalizada com base no nome da IA.
        """
        name_response = "Meu nome é Catelina Lacet! Sou uma IA geek, arquiteta e mãe de pet."
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
