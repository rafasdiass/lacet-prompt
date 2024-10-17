import spacy
import logging
from transformers import pipeline
from typing import Dict, Union
from services.gpt_service import GPTService

# Carregar o modelo spaCy para fallback local
nlp = spacy.load("en_core_web_sm")

# Definir pipeline local de fallback (Roberta para análise de sentimentos)
classifier = pipeline("sentiment-analysis", model="roberta-base")

class TextProcessingService:
    """
    Serviço responsável por enviar o prompt diretamente ao GPT-4,
    e usar análise local como fallback em caso de falha.
    """

    def __init__(self, gpt_service: GPTService):
        self.gpt_service = gpt_service  # Sempre utilizará o serviço GPT-4

    def clean_text(self, text: str) -> str:
        """
        Limpa o texto removendo caracteres especiais e números.
        """
        import re
        return re.sub(r"[^a-zA-Z\s]", "", text).strip().lower()

    def analyze_text(self, text: str) -> Dict[str, Union[str, list]]:
        """
        Fallback: Analisa o texto localmente usando spaCy e transformers.
        """
        try:
            logging.info(f"Analisando texto localmente: {text}")
            doc = nlp(text)
            sentiment = classifier(text)

            keywords = [token.text for token in doc]
            entities = [(ent.text, ent.label_) for ent in doc.ents]

            return {
                "keywords": keywords,
                "sentiment": sentiment[0]["label"],
                "entities": entities,
            }
        except Exception as e:
            logging.error(f"Erro ao analisar texto localmente: {str(e)}")
            return {"keywords": ["generico"], "sentiment": "NEUTRAL", "entities": []}

    def process_text(self, input_data: str) -> str:
        """
        Processa o texto fornecido e sempre tenta enviar primeiro para o GPT-4.
        Se falhar, faz o fallback para análise local.
        """
        cleaned_text = self.clean_text(input_data)

        # Primeiro, tenta usar o GPT-4
        try:
            logging.info("Enviando prompt para GPT-4")
            return self.gpt_service.enviar_prompt(cleaned_text)  # Sempre usar GPT-4
        except Exception as e:
            logging.error(f"Erro ao usar GPT-4: {str(e)}")
            logging.info("Usando fallback local")

        # Fallback: Análise local se o GPT falhar
        analysis = self.analyze_text(cleaned_text)
        return f"Fallback: {analysis['keywords']}"  # Simples fallback para análise de keywords
