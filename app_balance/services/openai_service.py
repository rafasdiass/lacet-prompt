# app_balance/services/openai_service.py
import openai
from environs import Env

# Carregar variáveis de ambiente para a chave da API do OpenAI
env = Env()
env.read_env()

# Verifica se a chave da API está definida
openai_key = env.str("OPENAI_API_KEY", default=None)
if openai_key:
    openai.api_key = openai_key
else:
    raise EnvironmentError("A chave da API do OpenAI não está definida. Verifique o arquivo .env")


def analyze_data(prompt: str) -> str:
    """
    Interage com a API do OpenAI para analisar dados com base no prompt fornecido
    utilizando a interface da API ChatCompletion.
    Se falhar, retorna uma resposta simulada.
    """
    if openai_key:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # ou "gpt-3.5-turbo"
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
            )
            # Retorna a resposta do GPT-4
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"Erro ao comunicar com o OpenAI: {str(e)}"
    else:
        return simulate_analyze_data(prompt)


def simulate_analyze_data(prompt: str) -> str:
    """
    Retorna uma análise simulada sem conexão com OpenAI.
    """
    return f"Simulação GPT-4: Baseado no prompt '{prompt}', aqui está a análise simulada dos dados financeiros."
