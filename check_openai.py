from openai import OpenAI
import openai
from environs import Env

# Carregar variáveis de ambiente
env = Env()
env.read_env()

# Definir a chave da API do OpenAI
openai_key = env.str("OPENAI_API_KEY", default=None)

# Verifica se a chave foi carregada corretamente
if openai_key:
    client = OpenAI(api_key=openai_key)  # Inicializar o cliente OpenAI aqui, depois de definir a chave da API

    print(f"OpenAI Library Version: {openai.__version__}")
    print(f"OpenAI Library Path: {openai.__file__}")

    try:
        # Testar a nova interface da API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Olá, GPT-4!"}],
            max_tokens=10
        )
        print("Chamada de teste bem-sucedida:", response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Erro ao comunicar com o GPT-4:\n{str(e)}")
else:
    print("A chave da API do OpenAI não está definida no arquivo .env.")
