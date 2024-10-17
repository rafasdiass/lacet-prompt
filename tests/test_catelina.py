import pytest
from unittest.mock import MagicMock
from app_balance.services.catelina_lacet import CatelinaLacetGPT

@pytest.fixture
def mock_data_persistence_service():
    """
    Mock do serviço de persistência de dados.
    """
    mock_service = MagicMock()
    mock_service.get_latest_financial_data.return_value = {
        "total_custos": 1000.0,
        "receita_projetada": 1500.0,
        "categorias_custos": {
            "Marketing": 500.0,
            "Desenvolvimento": 500.0
        }
    }
    return mock_service

@pytest.fixture
def mock_gpt_service():
    """
    Mock do serviço de integração com GPT.
    """
    mock_service = MagicMock()
    mock_service.enviar_prompt.return_value = "Resposta gerada pelo GPT-4"
    return mock_service

@pytest.fixture
def catelina_lacet(mock_data_persistence_service, mock_gpt_service):
    """
    Instancia a IA com o serviço de persistência de dados e o serviço GPT-4 mockados.
    """
    return CatelinaLacetGPT(tipo_humor="compreensivo", data_persistence_service=mock_data_persistence_service, gpt_service=mock_gpt_service)

@pytest.fixture
def catelina_lacet_sem_gpt(mock_data_persistence_service):
    """
    Instancia a IA com o serviço de persistência de dados e sem o GPT-4 configurado.
    """
    return CatelinaLacetGPT(tipo_humor="compreensivo", data_persistence_service=mock_data_persistence_service, gpt_service=None)

def test_generate_response_nome(catelina_lacet):
    """
    Testa a resposta quando a pergunta envolve o nome da IA.
    """
    analysis = {"keywords": []}
    prompt = "Qual é o seu nome?"

    resposta = catelina_lacet.generate_response(prompt, analysis)

    assert "Meu nome é Catelina Lacet!" in resposta

def test_generate_response_financeiro(catelina_lacet_sem_gpt, mock_data_persistence_service):
    """
    Testa a resposta quando o prompt envolve finanças usando a lógica local (sem GPT-4).
    """
    analysis = {"keywords": ["finance"]}
    prompt = "Qual é a minha receita projetada?"

    resposta = catelina_lacet_sem_gpt.generate_response(prompt, analysis)

    assert "Receita projetada: R$ 1500.00" in resposta
    assert "Total de custos: R$ 1000.00" in resposta
    assert "Marketing: R$ 500.00" in resposta

    mock_data_persistence_service.persist_data.assert_called_with(
        "financeiro",
        categorias_custos={"Marketing": 500.0, "Desenvolvimento": 500.0},
        total_custos=1000.0,
        receita_projetada=1500.0
    )

def test_generate_response_generica(catelina_lacet, mock_data_persistence_service):
    """
    Testa uma resposta genérica.
    """
    analysis = {"keywords": []}
    prompt = "Me conte sobre o filme De Volta Para o Futuro."

    resposta = catelina_lacet.generate_response(prompt, analysis)

    assert "Essa pergunta me lembrou um filme" in resposta

    mock_data_persistence_service.persist_data.assert_called_with(
        "prompt", prompt_text=prompt, response=resposta
    )

def test_generate_response_gpt(catelina_lacet, mock_gpt_service):
    """
    Testa a chamada bem-sucedida ao GPT-4 para uma resposta externa.
    """
    analysis = {"keywords": ["finance"]}
    prompt = "Me fale sobre finanças"

    # Verifique se a resposta é gerada pelo GPT-4
    resposta = catelina_lacet.generate_response(prompt, analysis)
    
    # Certifique-se de que a chamada ao GPT-4 foi feita
    mock_gpt_service.enviar_prompt.assert_called_once_with(prompt)
    
    # Verifique se a resposta é a esperada do GPT-4
    assert resposta == "Resposta gerada pelo GPT-4"

def test_generate_response_financeiro_sem_dados(catelina_lacet_sem_gpt, mock_data_persistence_service):
    """
    Testa o cenário onde não há dados financeiros recentes, usando a lógica local.
    """
    mock_data_persistence_service.get_latest_financial_data.return_value = None

    analysis = {"keywords": ["finance"]}
    prompt = "Me mostre os últimos dados financeiros."

    resposta = catelina_lacet_sem_gpt.generate_response(prompt, analysis)

    assert "Parece que ainda não tenho dados financeiros recentes para você." in resposta
