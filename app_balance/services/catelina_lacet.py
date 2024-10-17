import random
import logging
from app_balance.services.greeting_service import GreetingService

# Configurar logging
logging.basicConfig(level=logging.INFO)

class CatelinaLacetGPT:
    """
    IA simpática e bem-humorada que interpreta dados e os responde,
    com lógica híbrida para decidir quando persistir dados e quando usar GPT-4.
    """

    def __init__(self, tipo_humor: str = "padrao", data_persistence_service=None, gpt_service=None):
        self.tipo_humor = tipo_humor
        self.data_persistence_service = data_persistence_service  # Serviço de persistência de dados
        self.gpt_service = gpt_service  # Serviço de integração com GPT-4
        self.greeting_service = GreetingService()  # Instancia o serviço de saudações
        self.nome = "Catelina Lacet"
        self.idade = 45  # Atributo embutido de idade
        self.profissao = "IA geek, arquiteta e mãe de pet"

    def generate_response(self, prompt: str, analysis: dict) -> str:
        """
        Gera a resposta final para o prompt enviado, com base no que já foi processado (análise de texto ou finanças).
        """
        logging.info(f"Gerando resposta para o prompt: {prompt}")
        logging.info(f"Análise recebida: {analysis}")

        prompt_lower = prompt.lower()

        # Exemplo: Responder perguntas genéricas sobre a IA
        if "nome" in prompt_lower:
            return f"Meu nome é {self.nome}! Sou uma {self.profissao}. Vamos continuar, assim como Marty McFly seguiria a 88 milhas por hora!"

        # Prioriza o GPT-4 se houver um serviço GPT configurado e a análise tiver a palavra-chave "finance"
        if self.gpt_service and "finance" in analysis.get("keywords", []):
            logging.info("Tentando gerar resposta com GPT-4")
            try:
                return self.gpt_service.enviar_prompt(prompt)
            except Exception as e:
                logging.error(f"Erro ao usar GPT-4: {str(e)}")
                # Fallback para lógica financeira local em caso de falha

        # Verifica se o prompt é sobre finanças e obtém dados do serviço de persistência
        if self.is_financial_prompt(analysis):
            logging.info("Analisando finanças localmente")
            financial_data = self.data_persistence_service.get_latest_financial_data()

            if financial_data:
                response = self.formulate_financial_response(financial_data)

                # Persistir o dado financeiro processado
                self.data_persistence_service.persist_data(
                    "financeiro",
                    categorias_custos=financial_data["categorias_custos"],
                    total_custos=financial_data["total_custos"],
                    receita_projetada=financial_data["receita_projetada"]
                )

                return response
            else:
                return "Parece que ainda não tenho dados financeiros recentes para você. Envie-me suas finanças para análise!"

        # Gera resposta local para perguntas genéricas
        response = self.formulate_generic_or_funny_response(prompt)

        # Persistir o prompt após gerar a resposta
        if self.tipo_humor != "sarcastico":
            self.data_persistence_service.persist_data("prompt", prompt_text=prompt, response=response)

        return response

    def is_financial_prompt(self, analysis: dict) -> bool:
        """Verifica se o prompt é relacionado a finanças, com base na análise prévia."""
        return "finance" in analysis.get("keywords", [])

    def formulate_financial_response(self, financial_data: dict) -> str:
        """Formula uma resposta com base nos dados financeiros já processados."""
        receita = financial_data.get("receita_projetada", 0)
        custos = financial_data.get("total_custos", 0)
        categorias = financial_data.get("categorias_custos", {})

        resposta = f"Receita projetada: R$ {receita:.2f}\nTotal de custos: R$ {custos:.2f}\nCategorias de custos:\n"
        for categoria, valor in categorias.items():
            resposta += f"- {categoria}: R$ {valor:.2f}\n"

        # Adiciona uma frase de humor
        if self.tipo_humor == "sarcastico":
            resposta += "Espero que você tenha algo sobrando depois desses gastos todos!"
        elif self.tipo_humor == "compreensivo":
            resposta += "Vamos superar esses desafios financeiros juntos."

        return resposta

    def formulate_generic_or_funny_response(self, prompt: str) -> str:
        """Gera uma resposta genérica ou engraçada."""
        generic_responses = [
            "Essa pergunta me lembrou um filme... já assistiu 'De Volta para o Futuro'?"
        ]
        return random.choice(generic_responses)
