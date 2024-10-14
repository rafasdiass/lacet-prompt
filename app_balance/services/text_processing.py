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
    Agora também inclui a capacidade de detectar perguntas genéricas ou confusas.
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
        self.generic_keywords = [
            "nome",
            "idade",
            "filme",
            "herói",
            "gosta",
            "hobby",
            "filmes",
            "personagem",
        ]  # Palavras associadas a perguntas genéricas
        self.context_generic = [
            "me fale sobre",
            "quem é",
            "o que é",
        ]  # Frases genéricas

    def clean_text(self, text: str) -> str:
        """
        Limpa o texto removendo caracteres especiais e números.
        """
        import re

        text = re.sub(r"[^a-zA-Z\s]", "", text)
        return text.strip().lower()

    def analyze_text(self, text: str) -> dict:
        """
        Analisa o texto usando spaCy e Transformers para identificar categorias, sentimento e palavras-chave.
        Também detecta se a pergunta é genérica.
        """
        try:
            doc = nlp(text)
            sentiment = classifier(text)

            # Extrair entidades e tokens do texto
            keywords = [token.text for token in doc]
            entities = [(ent.text, ent.label_) for ent in doc.ents]

            # Detectar se é uma pergunta genérica
            is_generic = self.is_generic_prompt(text)

            return {
                "keywords": keywords,
                "sentiment": sentiment[0]["label"],
                "entities": entities,
                "is_generic": is_generic,  # Novo campo para identificar perguntas genéricas
            }
        except Exception as e:
            logging.error(f"Erro ao analisar o texto: {str(e)}")
            return {
                "keywords": [],
                "sentiment": "NEUTRAL",
                "entities": [],
                "is_generic": False,  # Considera que não é genérico em caso de erro
                "error": str(e),
            }

    def is_generic_prompt(self, text: str) -> bool:
        """
        Verifica se a pergunta é genérica, baseando-se em palavras-chave e frases padrão.

        Args:
            text (str): Texto da pergunta enviada pelo usuário.

        Returns:
            bool: Verdadeiro se a pergunta for genérica, falso caso contrário.
        """
        # Limpar e padronizar o texto para facilitar a detecção
        cleaned_text = self.clean_text(text)

        # Detectar se o texto contém palavras-chave genéricas
        if any(keyword in cleaned_text for keyword in self.generic_keywords):
            return True

        # Detectar se o texto contém frases genéricas
        if any(phrase in cleaned_text for phrase in self.context_generic):
            return True

        return False

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
        Agora leva em consideração se a pergunta é genérica.
        """
        keywords = analysis.get("keywords", [])

        # Verifica se é um prompt genérico
        if analysis.get("is_generic"):
            return "generic"

        # Se não for genérico, verifica se é uma pergunta financeira ou de piada
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
