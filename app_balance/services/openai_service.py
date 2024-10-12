# -*- coding: utf-8 -*-
"""Serviço para interação com o OpenAI."""
import openai
from environs import Env

# Carregar variáveis de ambiente para a chave da API do OpenAI
env = Env()
env.read_env()

# Configurar a chave de API do OpenAI
openai.api_key = env.str("OPENAI_API_KEY")

def analyze_data(prompt: str) -> str:
    """Interage com a API do OpenAI para analisar dados com base no prompt fornecido."""
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
