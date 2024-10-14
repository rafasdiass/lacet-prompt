import random
from imdb import IMDb
import pyjokes
from app_balance.services.greeting_service import GreetingService


class CatelinaLacetGPT:
    """
    IA simpática e bem-humorada que interpreta dados e os responde, sem processar nada diretamente.
    Respostas são formuladas com base no humor e nas interações passadas.
    """

    def __init__(self, tipo_humor: str = "padrao"):
        self.tipo_humor = tipo_humor
        self.greeting_service = GreetingService()  # Instancia o serviço de saudações
        self.imdb = IMDb()  # Para buscar referências de filmes e cultura pop
        self.joke_provider = pyjokes  # Para gerar piadas baseadas em humor
        self.filmes_favoritos = [
            "De Volta para o Futuro",
            "Star Wars",
            "Matrix",
            "O Senhor dos Anéis",
        ]
        self.movie_cache = []  # Cache para armazenar dados de filmes

    def generate_response(
        self, prompt: str, analysis: dict, financial_data=None
    ) -> str:
        """
        Gera a resposta final para o prompt enviado, com base no que já foi processado (análise de texto ou finanças).

        Args:
            prompt (str): O prompt original enviado pelo usuário.
            analysis (dict): Resultado da análise pré-processada do TextProcessingService.
            financial_data (dict, optional): Dados financeiros processados.

        Returns:
            str: Resposta gerada pela Catelina Lacet.
        """
        # Se for uma saudação, retorna uma resposta de saudação
        if self.greeting_service.is_greeting(prompt):
            return self.greeting_service.get_greeting_response(
                analysis.get("sentiment", "NEUTRAL")
            )

        # Se for relacionado a finanças, retorna a resposta financeira
        if self.is_financial_prompt(analysis):
            if financial_data:
                return self.formulate_financial_response(financial_data)
            else:
                return "Estou pronta para ajudar com suas finanças! Envie-me os dados necessários."

        # Caso contrário, retorna uma resposta geral
        return self.formulate_general_response(prompt, analysis)

    def is_financial_prompt(self, analysis: dict) -> bool:
        """
        Verifica se o prompt é relacionado a finanças, com base na análise prévia.

        Args:
            analysis (dict): Análise pré-processada do prompt.

        Returns:
            bool: Verdadeiro se o prompt for financeiro, falso caso contrário.
        """
        return "finance" in analysis.get("categories", [])

    def formulate_financial_response(self, financial_data: dict) -> str:
        """
        Formula uma resposta com base nos dados financeiros já processados.

        Args:
            financial_data (dict): Dados financeiros processados.

        Returns:
            str: Resposta com análise financeira.
        """
        receita = financial_data.get("receita_projetada", 0)
        custos = financial_data.get("total_custos", 0)
        categorias = financial_data.get("categorias_custos", {})

        # Formula a resposta financeira
        resposta = f"Receita projetada: R$ {receita:.2f}\n"
        resposta += f"Total de custos: R$ {custos:.2f}\n"

        resposta += "Categorias de custos:\n"
        for categoria, valor in categorias.items():
            resposta += f"- {categoria}: R$ {valor:.2f}\n"

        # Adiciona uma frase de humor, dependendo do humor atual da IA
        if self.tipo_humor == "sarcastico":
            resposta += (
                "\nEspero que você tenha algo sobrando depois desses gastos todos!"
            )
        elif self.tipo_humor == "compreensivo":
            resposta += (
                "\nNão se preocupe, vamos superar esses desafios financeiros juntos."
            )

        return resposta

    def formulate_general_response(self, prompt: str, analysis: dict) -> str:
        """
        Formula uma resposta geral baseada na análise do prompt, com humor e cultura pop.

        Args:
            prompt (str): O prompt original enviado pelo usuário.
            analysis (dict): Análise pré-processada do prompt.

        Returns:
            str: Resposta formulada de forma geral.
        """
        resposta = f"Sua pergunta foi sobre: {analysis.get('keywords', [])}\n"

        # Adiciona uma piada ou uma referência de filme
        if self.tipo_humor == "sarcastico":
            resposta += f"Ah, claro... {self.joke_provider.get_joke()}"
        else:
            resposta += f"Já assistiu {random.choice(self.filmes_favoritos)}? Pode ser uma boa distração!"

        return resposta
