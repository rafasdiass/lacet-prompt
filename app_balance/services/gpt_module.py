from app_balance.services.openai_service import analyze_data
from typing import Dict

class CatelinaLacetGPT:
    """
    A simpática e bem-humorada IA 'Catelina Lacet' que usa GPT-4 para fornecer análises
    financeiras com referências divertidas a filmes, heróis, cultura pop e humor.
    Ela mistura dados financeiros complexos com uma abordagem leve e divertida.
    """

    def __init__(self, tipo_humor: str = 'padrao'):
        self.tipo_humor = tipo_humor

    def generate_gpt_response(self, prompt: str) -> str:
        """
        Gera uma resposta usando GPT-4, chamando a função no serviço `openai_service`.

        Args:
            prompt (str): O prompt de entrada para gerar a resposta.

        Returns:
            str: A resposta gerada pelo GPT-4.
        """
        return analyze_data(prompt)

    def generate_dynamic_references(self) -> str:
        """
        Gera uma resposta GPT-4 que inclui citações e referências aleatórias sobre filmes,
        heróis e cultura pop, com foco em finanças e negócios, adaptando ao tipo de humor.

        Returns:
            str: Uma resposta gerada dinamicamente usando o GPT-4.
        """
        prompt = self._gerar_prompt_referencias()
        return self.generate_gpt_response(prompt)

    def _gerar_prompt_referencias(self) -> str:
        """
        Gera o prompt de referências dinâmicas baseado no tipo de humor do usuário.

        Returns:
            str: O prompt que será enviado ao GPT-4 para gerar a resposta.
        """
        base_prompt = """
        Imagine que você é uma IA bem-humorada chamada Catelina Lacet, e você está prestes a dar conselhos financeiros importantes. 
        Misture referências a filmes dos anos 80, super-heróis e cultura pop enquanto fala sobre finanças e economia. 
        Faça isso de uma forma leve e divertida.
        """
        if self.tipo_humor == 'sarcastico':
            return base_prompt + """
            Adicione um toque sarcástico. Imagine como seria se Tony Stark desse conselhos financeiros, sempre com um tom de ironia.
            """
        elif self.tipo_humor == 'compreensivo':
            return base_prompt + """
            Adicione uma abordagem compreensiva e de apoio emocional. Como se a Mulher Maravilha estivesse ajudando alguém a lidar com seus desafios financeiros, sempre com empatia.
            """
        else:
            return base_prompt + """
            Seja divertida, mas mantenha a clareza e objetividade. Pense em uma mistura de Peter Parker e Marty McFly dando conselhos sobre como equilibrar as finanças.
            """

    def definir_tipo_humor(self, tipo_humor: str):
        """
        Define o tipo de humor para a IA Catelina Lacet.

        Args:
            tipo_humor (str): O tipo de humor ('sarcastico', 'compreensivo', 'padrao').
        """
        tipos_validos = ['sarcastico', 'compreensivo', 'padrao']
        if tipo_humor in tipos_validos:
            self.tipo_humor = tipo_humor
        else:
            raise ValueError(f"Tipo de humor inválido. Escolha entre: {', '.join(tipos_validos)}.")
