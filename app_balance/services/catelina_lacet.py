import logging
from app_balance.services.greeting_service import GreetingService

class CatelinaLacetGPT:
    """
    IA simpática e bem-humorada que interpreta dados e gera respostas.
    Usa GPT-4 para processar respostas e ajusta com seu toque pessoal.
    """

    def __init__(self, tipo_humor: str = "padrao"):
        self.tipo_humor = tipo_humor
        self.greeting_service = GreetingService()  # Serviço de saudações
        self.nome = "Catelina Lacet"
        self.idade = 45  # Atributo embutido de idade
        self.profissao = "IA geek, arquiteta e mãe de pet"

    def generate_response(self, gpt_response: str) -> str:
        """
        Gera a resposta final com base no que foi processado pelo GPT-4.
        Adiciona um toque de humor ou contexto.
        """
        logging.info(f"Gerando resposta final a partir da resposta GPT: {gpt_response}")

        # Adiciona uma frase humorística dependendo do tipo de humor
        if self.tipo_humor == "sarcastico":
            return f"{gpt_response} - Isso, se você conseguir entender algo disso!"
        elif self.tipo_humor == "compreensivo":
            return f"{gpt_response} - Vamos superar isso juntos, passo a passo."
        else:
            return f"{gpt_response} - Continue assim, você está indo muito bem!"
