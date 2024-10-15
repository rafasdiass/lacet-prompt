from openai import OpenAI
from environs import Env

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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Em caso de erro, apenas retorna uma resposta genérica sem depender de GPT-4
        return ""  # Não deve causar impacto na resposta final, o GPT-4 é apenas um complemento
