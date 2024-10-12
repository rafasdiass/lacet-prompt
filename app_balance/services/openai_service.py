import openai
from environs import Env

# Carregar variáveis de ambiente para a chave da API do OpenAI
env = Env()
env.read_env()

# Verifica se a chave da API está definida
openai_key = env.str("OPENAI_API_KEY", default=None)
if openai_key:
    openai.api_key = openai_key

def analyze_data(prompt: str) -> str:
    """
    Tenta interagir com a API do OpenAI para analisar dados com base no prompt fornecido.
    Se falhar, retorna uma resposta simulada.
    """
    if openai_key:
        try:
            response = openai.Completion.create(
                engine="text-davinci-004",  # Pode ser "gpt-4" dependendo do setup
                prompt=prompt,
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Erro ao comunicar com o OpenAI: {str(e)}"
    else:
        return simulate_analyze_data(prompt)

def simulate_analyze_data(prompt: str) -> str:
    """
    Retorna uma análise simulada sem conexão com OpenAI.
    """
    return f"Simulação GPT-4: Baseado no prompt '{prompt}', aqui está a análise simulada dos dados financeiros."
