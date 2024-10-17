import random
from imdb import IMDb
import pyjokes
from app_balance.services.greeting_service import GreetingService
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

class CatelinaLacetGPT:
    """
    IA simpática e bem-humorada que interpreta dados e os responde, sem processar nada diretamente.
    Respostas são formuladas com base no humor e nas interações passadas.
    """

    def __init__(self, tipo_humor: str = "padrao", data_persistence_service=None):
        self.tipo_humor = tipo_humor
        self.data_persistence_service = data_persistence_service  # Serviço de persistência de dados
        self.greeting_service = GreetingService()  # Instancia o serviço de saudações
        self.imdb = IMDb()  # Para buscar referências de filmes e cultura pop
        self.joke_provider = pyjokes  # Para gerar piadas baseadas em humor
        self.filmes_favoritos = [
            "De Volta para o Futuro",
            "Star Wars",
            "Matrix",
            "O Senhor dos Anéis",
        ]
        self.hobbies = [
            "ler livros de arquitetura",
            "assistir filmes de ficção científica",
            "cuidar do meu pet",
        ]
        self.personalidades_favoritas = ["Marty McFly", "Leia Organa", "Neo"]
        self.movie_cache = []  # Cache para armazenar dados de filmes
        self.nome = "Catelina Lacet"
        self.idade = 45  # Atributo embutido de idade
        self.profissao = "IA geek, arquiteta e mãe de pet"

    def generate_response(self, prompt: str, analysis: dict) -> str:
        """
        Gera a resposta final para o prompt enviado, com base no que já foi processado (análise de texto ou finanças).

        Args:
            prompt (str): O prompt original enviado pelo usuário.
            analysis (dict): Resultado da análise pré-processada do TextProcessingService.

        Returns:
            str: Resposta gerada pela Catelina Lacet.
        """
        logging.info(f"Gerando resposta para o prompt: {prompt}")
        logging.info(f"Análise recebida: {analysis}")

        prompt_lower = prompt.lower()

        # Responder perguntas genéricas sobre a IA, como nome, idade e profissão
        if "nome" in prompt_lower:
            return f"Meu nome é {self.nome}! Sou uma {self.profissao}. Vamos continuar, assim como Marty McFly seguiria a 88 milhas por hora!"

        if "idade" in prompt_lower:
            return f"Eu tenho {self.idade} anos! E você, já assistiu Star Wars? Pode ser uma boa distração!"

        if "filme" in prompt_lower or "filmes" in prompt_lower:
            return f"Eu adoro {random.choice(self.filmes_favoritos)}! É um dos meus filmes preferidos. E você?"

        if "gosta" in prompt_lower or "hobby" in prompt_lower:
            return f"Eu adoro {random.choice(self.hobbies)} nas horas vagas! O que você gosta de fazer?"

        if "herói" in prompt_lower or "personagem" in prompt_lower:
            return f"Meu herói favorito? Com certeza {random.choice(self.personalidades_favoritas)}! Eles sempre me inspiram a seguir em frente."

        # Verifica se o prompt é sobre finanças e obtém dados do serviço de persistência
        if self.is_financial_prompt(analysis):
            logging.info("Analisando finanças")
            if not self.data_persistence_service:
                logging.error("Serviço de persistência de dados não foi inicializado corretamente.")
                return "Desculpe, estou enfrentando problemas técnicos ao tentar acessar os dados financeiros."
            
            financial_data = self.data_persistence_service.get_latest_financial_data()
            if financial_data:
                return self.formulate_financial_response(financial_data)
            else:
                logging.warning("Sem dados financeiros recentes.")
                return "Parece que ainda não tenho dados financeiros recentes para você. Envie-me suas finanças para análise!"

        # Caso a pergunta não faça sentido ou seja confusa
        return self.formulate_generic_or_funny_response(prompt)

    def is_financial_prompt(self, analysis: dict) -> bool:
        """
        Verifica se o prompt é relacionado a finanças, com base na análise prévia.
        """
        logging.info("Verificando se o prompt é financeiro.")
        return "finance" in analysis.get("keywords", [])

    def formulate_financial_response(self, financial_data: dict) -> str:
        """
        Formula uma resposta com base nos dados financeiros já processados.
        """
        logging.info(f"Formulando resposta financeira com dados: {financial_data}")

        receita = financial_data.get("receita_projetada", 0)
        custos = financial_data.get("total_custos", 0)
        categorias = financial_data.get("categorias_custos", {})

        resposta = f"Receita projetada: R$ {receita:.2f}\n"
        resposta += f"Total de custos: R$ {custos:.2f}\n"
        resposta += "Categorias de custos:\n"
        for categoria, valor in categorias.items():
            resposta += f"- {categoria}: R$ {valor:.2f}\n"

        # Adiciona uma frase de humor, dependendo do humor atual da IA
        if self.tipo_humor == "sarcastico":
            resposta += "\nEspero que você tenha algo sobrando depois desses gastos todos!"
        elif self.tipo_humor == "compreensivo":
            resposta += "\nNão se preocupe, vamos superar esses desafios financeiros juntos."

        return resposta

    def formulate_generic_or_funny_response(self, prompt: str) -> str:
        """
        Gera uma resposta genérica ou engraçada caso a pergunta seja confusa ou sem sentido.
        """
        generic_responses = [
            "Hmm, isso me pegou de surpresa! O que você acha sobre o assunto?",
            "Não sei se entendi bem, mas me parece algo interessante!",
            "Essa pergunta me lembra um filme... já assistiu 'De Volta para o Futuro'?",
            "Sabe, às vezes as melhores respostas são aquelas que encontramos dentro de nós. Ou talvez num filme do Star Wars.",
        ]

        funny_responses = [
            f"Você disse '{prompt}'? Isso me lembrou uma piada! {self.joke_provider.get_joke()}",
            "Olha, com essa pergunta confusa, até Marty McFly ficaria perdido no tempo!",
            "Hmm, não sei bem como responder isso... que tal falarmos sobre filmes?",
        ]

        # Retorna uma resposta engraçada ou genérica dependendo do humor
        if self.tipo_humor == "sarcastico":
            return random.choice(funny_responses)
        else:
            return random.choice(generic_responses)
