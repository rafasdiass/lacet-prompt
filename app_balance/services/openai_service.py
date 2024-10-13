from openai import OpenAI
from environs import Env
from app_balance.models import Recebimento
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Configuração do banco de dados
DATABASE_URL = 'sqlite:///recebimentos.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Carregar variáveis de ambiente para as configurações do OpenAI
env = Env()
env.read_env()

openai_key = env.str("OPENAI_API_KEY", default=None)
organization_id = env.str("OPENAI_ORG_ID", default=None)

if not openai_key:
    raise EnvironmentError("A chave da API do OpenAI não está definida. Verifique o arquivo .env")

if not organization_id:
    raise EnvironmentError("O ID da organização do OpenAI não está definido. Verifique o arquivo .env")

# Instancia o cliente da API OpenAI com a chave e o ID da organização
client = OpenAI(api_key=openai_key, organization=organization_id)

def analyze_data_with_fallback(prompt: str) -> str:
    """
    Combina dados locais com uma resposta da OpenAI para criar uma resposta inteligente.
    Prioriza dados locais e usa o GPT-4 como complemento.
    """
    local_data = get_local_data(prompt)
    enriched_data = ""

    try:
        # Tentando enriquecer com GPT-4, mas sem depender totalmente dele
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        enriched_data = response.choices[0].message.content.strip()
    except Exception:
        enriched_data = ""  # Caso o GPT-4 não esteja disponível, não faz diferença para o usuário
    
    # Combina os dados locais com o enriquecimento do GPT-4
    return f"{local_data} {enriched_data}".strip()  # Retorna sempre a resposta local e, se disponível, complementa com o GPT-4

def get_local_data(prompt: str) -> str:
    """
    Responde com dados locais, priorizando informações já armazenadas no banco de dados.
    """
    if "qual seu nome" in prompt.lower():
        return "Meu nome é Catelina Lacet! Sou uma IA geek, arquiteta, mãe de pet e pronta para te ajudar com suas finanças."

    # Utiliza dados do banco de dados de recebimentos
    recebimentos = session.query(Recebimento).all()
    if recebimentos:
        total_recebimentos = sum([r.valor for r in recebimentos])
        return f"De acordo com os dados locais, o total de recebimentos é de R$ {total_recebimentos:.2f}. "
    
    # Caso não tenha dados, uma resposta amigável é retornada
    return "Ainda não tenho dados financeiros detalhados, mas estou pronta para aprender mais com você!"
