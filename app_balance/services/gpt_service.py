import logging
try:
    import openai
except ImportError as e:
    logging.error("O pacote 'openai' não foi encontrado. Certifique-se de que ele está instalado.")
    raise e

class GPTService:
    """
    Serviço para gerenciar a comunicação com o GPT-4.
    """

    def __init__(self, api_key):
        openai.api_key = api_key

    def enviar_prompt(self, prompt: str) -> str:
        """
        Envia um prompt para o GPT-4 e retorna a resposta.
        """
        try:
            logging.info(f"Enviando prompt para GPT-4: {prompt}")
            response = openai.Completion.create(
                model="gpt-4",
                prompt=prompt,
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            logging.error(f"Erro ao comunicar com GPT-4: {str(e)}")
            return "Desculpe, houve um erro ao processar sua solicitação."
