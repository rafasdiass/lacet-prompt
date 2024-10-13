from openai import OpenAI
from environs import Env
from app_balance.models import Recebimento  # Importar o modelo Recebimento
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

# Verifica se a chave da API e o ID da organização estão definidos
openai_key = env.str("OPENAI_API_KEY", default=None)
organization_id = env.str("OPENAI_ORG_ID", default=None)

if not openai_key:
    raise EnvironmentError("A chave da API do OpenAI não está definida. Verifique o arquivo .env")

if not organization_id:
    raise EnvironmentError("O ID da organização do OpenAI não está definido. Verifique o arquivo .env")

# Instancia o cliente da API OpenAI com a chave e o ID da organização
client = OpenAI(api_key=openai_key, organization=organization_id)

def analyze_data(prompt: str) -> str:
    """
    Interage com a API do OpenAI para analisar dados com base no prompt fornecido.
    Se falhar por excesso de cota, retorna uma resposta simulada.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Altere para o modelo compatível
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Se for erro de cota, usar dados locais
        if 'insufficient_quota' in str(e):
            return simulate_analyze_data(prompt)
        else:
            return f"Erro ao comunicar com o OpenAI: {str(e)}"

def simulate_analyze_data(prompt: str) -> str:
    """
    Retorna uma análise simulada usando dados locais.
    """
    # Integração com dados do banco de dados
    recebimentos = session.query(Recebimento).all()
    if recebimentos:
        total_recebimentos = sum([r.valor for r in recebimentos])
        return f"A resposta baseada nos dados locais: total de recebimentos é R$ {total_recebimentos:.2f}."
    else:
        return f"Baseado no prompt '{prompt}', não há dados locais disponíveis."
