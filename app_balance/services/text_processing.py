import spacy
from transformers import pipeline
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Carregar modelo do spaCy e Transformers
nlp = spacy.load("en_core_web_sm")
classifier = pipeline("sentiment-analysis")


class TextProcessingService:
    """
    Serviço responsável por processar textos e dados extraídos, interpretar linguagem natural, e decidir a rota apropriada.
    """

    def __init__(self):
        # Define as palavras-chave importantes para as rotas
        self.financial_keywords = [
            "finança",
            "investimento",
            "dinheiro",
            "ações",
            "economia",
        ]
        self.joke_keywords = ["piada", "engraçado", "brincadeira"]

    def clean_text(self, text: str) -> str:
        """
        Limpa o texto removendo caracteres especiais e números.
        """
        import re

        text = re.sub(r"[^a-zA-Z\s]", "", text)
        return text.strip().lower()

    def analyze_text(self, text: str) -> dict:
        """
        Analisa o texto usando spaCy e Transformers.
        """
        try:
            doc = nlp(text)
            sentiment = classifier(text)

            return {
                "keywords": [token.text for token in doc],
                "sentiment": sentiment[0]["label"],
                "entities": [(ent.text, ent.label_) for ent in doc.ents],
            }
        except Exception as e:
            logging.error(f"Erro ao analisar o texto: {str(e)}")
            return {
                "keywords": [],
                "sentiment": "NEUTRAL",
                "entities": [],
                "error": str(e),
            }

    def process_data_from_file(self, data: dict) -> dict:
        """
        Processa os dados extraídos de arquivos e os converte para um formato adequado para análise de texto.
        """
        text_representation = " ".join(
            [f"{cat} {val}" for cat, val in data["categorias_custos"].items()]
        )
        return self.analyze_text(text_representation)

    def decide_route(self, analysis: dict) -> str:
        """
        Decide a rota com base na análise do texto ou dados.
        """
        keywords = analysis.get("keywords", [])

        if any(keyword in self.financial_keywords for keyword in keywords):
            return "financial"
        elif any(keyword in self.joke_keywords for keyword in keywords):
            return "joke"
        else:
            return "general"

    def route_and_process(self, input_data: dict) -> str:
        """
        Processa tanto textos fornecidos diretamente pelo input do usuário quanto dados extraídos de arquivos.
        """
        if isinstance(input_data, str):
            # Se a entrada for texto, processa como texto
            cleaned_text = self.clean_text(input_data)
            analysis = self.analyze_text(cleaned_text)
        else:
            # Se for um dicionário, processa como dados de arquivo
            analysis = self.process_data_from_file(input_data)

        # Decide a rota com base na análise
        route = self.decide_route(analysis)
        logging.info(f"Rota decidida: {route}")
        return route
