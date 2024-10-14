import spacy
from textblob import TextBlob
from transformers import pipeline
import logging
import nltk

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Baixar recursos para TextBlob e nltk
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# Carregar modelo do Spacy e Transformers
nlp = spacy.load("en_core_web_sm")
classifier = pipeline('sentiment-analysis')


class TextProcessingService:
    """
    Serviço responsável por analisar o texto do prompt e determinar a rota apropriada com base em palavras-chave.
    """

    def __init__(self):
        pass

    def clean_prompt(self, prompt: str) -> str:
        """
        Limpa o prompt removendo caracteres especiais e números.
        """
        import re
        prompt = re.sub(r'[^a-zA-Z\s]', '', prompt)
        return prompt.strip().lower()

    def analyze_text(self, prompt: str) -> dict:
        """
        Analisa o texto do prompt usando TextBlob, Spacy e Transformers.
        """
        try:
            blob = TextBlob(prompt)
            doc = nlp(prompt)
            sentiment = classifier(prompt)

            return {
                'keywords': list(set(blob.noun_phrases)),
                'sentiment': sentiment[0]['label'],
                'entities': [(ent.text, ent.label_) for ent in doc.ents],
                'pos_tags': [(token.text, token.pos_) for token in doc]
            }
        except Exception as e:
            logging.error(f"Erro ao analisar o texto: {str(e)}")
            return {
                'keywords': [],
                'sentiment': 'NEUTRAL',
                'entities': [],
                'pos_tags': [],
                'error': str(e)
            }

    def decide_route(self, prompt: str, analysis: dict) -> str:
        """
        Decide a rota com base na análise do texto.
        """
        if 'finança' in analysis['keywords'] or 'dinheiro' in analysis['keywords']:
            return 'financial' if 'avançada' not in prompt else 'advanced_financial'
        elif 'piada' in analysis['keywords']:
            return 'joke'
        else:
            return 'general'

    def route_and_process(self, prompt: str) -> str:
        """
        Processa o prompt, realiza a análise de texto, e decide qual rota seguir.

        Args:
            prompt: Texto do prompt.

        Returns:
            str: Rota decidida com base na análise do prompt.
        """
        cleaned_prompt = self.clean_prompt(prompt)
        analysis = self.analyze_text(cleaned_prompt)
        route = self.decide_route(cleaned_prompt, analysis)
        logging.info(f"Rota: {route}")
        return route
