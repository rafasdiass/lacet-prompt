from openai import OpenAI
from environs import Env
import logging

# Configurações da API OpenAI
env = Env()
env.read_env()

openai_key = env.str("OPENAI_API_KEY", default=None)
organization_id = env.str("OPENAI_ORG_ID", default=None)

if not openai_key:
    raise EnvironmentError("A chave da API do OpenAI não está definida. Verifique o arquivo .env")
if not organization_id:
    raise EnvironmentError("O ID da organização do OpenAI não está definido. Verifique o arquivo .env")

client = OpenAI(api_key=openai_key, organization=organization_id)

def analyze_data(prompt: str) -> str:
    """
    Envia o prompt para o GPT-4 e retorna a resposta.
    Se houver um erro, retorna uma resposta padrão baseada em dados locais.
    """
    try:
        logging.info(f"Enviando prompt para GPT-4: {prompt}")
        response = client.chat.completions.create(
            model="gpt-4",  # Use GPT-4 aqui
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Erro ao comunicar com GPT-4: {str(e)}")
        # Em caso de erro, retorna uma resposta padrão
        return "Desculpe, houve um erro ao processar sua solicitação."
