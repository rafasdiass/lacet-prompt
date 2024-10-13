from openai import OpenAI
from environs import Env
from typing import Dict
from .financial_analysis import FinancialAnalysisService

# Carregar variáveis de ambiente para a chave da API do OpenAI
env = Env()
env.read_env()

# Definir a chave da API do OpenAI
client = OpenAI(api_key=env.str("OPENAI_API_KEY"))

class CatelinaLacetGPT:
    """
    A simpática e bem-humorada IA 'Catelina Lacet' que usa GPT-4 para fornecer análises
    financeiras com referências divertidas a filmes, heróis, cultura pop e humor.
    Ela mistura dados financeiros complexos com uma abordagem leve e divertida.
    """

    def __init__(self, tipo_humor: str = 'padrao'):
        self.financial_service = FinancialAnalysisService()
        self.tipo_humor = tipo_humor

    def generate_gpt_response(self, prompt: str) -> str:
        """
        Gera uma resposta usando GPT-4.

        Args:
            prompt (str): O prompt de entrada para gerar a resposta.

        Returns:
            str: A resposta gerada pelo GPT-4.
        """
        try:
            response = client.chat.completions.create(
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
            No entanto, adicione um toque sarcástico. Imagine como seria se Tony Stark desse conselhos financeiros, sempre com um tom de ironia.
            """
        elif self.tipo_humor == 'compreensivo':
            return base_prompt + """
            Adicione uma abordagem compreensiva e de apoio emocional. Como se a Mulher Maravilha estivesse ajudando alguém a lidar com seus desafios financeiros, sempre com empatia.
            """
        else:
            return base_prompt + """
            Seja divertida, mas mantenha a clareza e objetividade. Pense em uma mistura de Peter Parker e Marty McFly dando conselhos sobre como equilibrar as finanças.
            """

    def get_financial_analysis(self, custos: Dict, receita_projetada: float, valor_hora: float, categorias_custos: Dict) -> str:
        """
        Realiza a análise financeira e usa o GPT-4 para adicionar insights criativos e divertidos,
        considerando o tipo de humor escolhido.

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
        prompt = f"Aqui está uma análise financeira: {analysis}. Adicione uma visão divertida e útil com referências de cultura pop e filmes."

        # Gera resposta usando GPT-4
        gpt_response = self.generate_gpt_response(prompt)

        # Combina a resposta da análise financeira com humor e citações dinâmicas
        dynamic_references = self.generate_dynamic_references()

        return f"{gpt_response}\n\nAlém disso, Catelina Lacet diz: {dynamic_references}"

    def provide_financial_tips(self) -> str:
        """
        Gera dicas financeiras com uma abordagem divertida, adaptada ao tipo de humor.

        Returns:
            str: Dicas financeiras misturadas com cultura pop.
        """
        prompt = self._gerar_prompt_tips()
        return self.generate_gpt_response(prompt)

    def _gerar_prompt_tips(self) -> str:
        """
        Gera o prompt de dicas financeiras com base no tipo de humor do usuário.

        Returns:
            str: O prompt para gerar dicas financeiras.
        """
        base_prompt = """
        Você é a Catelina Lacet, uma IA cheia de personalidade e humor. 
        Compartilhe 3 dicas financeiras essenciais, mas faça isso de maneira leve, 
        usando referências a filmes clássicos, heróis ou cultura pop.
        """

        if self.tipo_humor == 'sarcastico':
            return base_prompt + """
            Adicione bastante sarcasmo, como se você fosse Tony Stark explicando as finanças para alguém que "claramente" não entende nada.
            """
        elif self.tipo_humor == 'compreensivo':
            return base_prompt + """
            Adote uma abordagem compreensiva, como a Mulher Maravilha, que se preocupa com o bem-estar financeiro de seus amigos.
            """
        else:
            return base_prompt + """
            Seja divertida e clara, como se Peter Parker estivesse explicando como economizar para o futuro.
            """

    def get_investment_advice(self) -> str:
        """
        Gera conselhos de investimento com humor e sabedoria financeira, adaptando ao tipo de humor.

        Returns:
            str: Um conselho de investimento divertido e prático.
        """
        prompt = self._gerar_prompt_investment_advice()
        return self.generate_gpt_response(prompt)

    def _gerar_prompt_investment_advice(self) -> str:
        """
        Gera o prompt de conselhos de investimento baseado no tipo de humor do usuário.

        Returns:
            str: O prompt para gerar conselhos de investimento.
        """
        base_prompt = """
        Como a Catelina Lacet, dê um conselho de investimento inteligente e bem-humorado. 
        Misture isso com referências a heróis da Marvel, Star Wars ou filmes dos anos 80 e 90. 
        Não esqueça de adicionar uma pitada de humor enquanto você fala sobre as vantagens 
        de diversificar os investimentos.
        """

        if self.tipo_humor == 'sarcastico':
            return base_prompt + """
            Adicione um tom sarcástico, como Tony Stark explicando que diversificar os investimentos é algo que "até o Jarvis já teria feito".
            """
        elif self.tipo_humor == 'compreensivo':
            return base_prompt + """
            Adote uma abordagem compreensiva, como se a Mulher Maravilha estivesse tranquilizando alguém sobre como diversificar pode ajudar a longo prazo.
            """
        else:
            return base_prompt + """
            Seja direto e divertido, como se Marty McFly estivesse explicando como investir para garantir um futuro melhor.
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
