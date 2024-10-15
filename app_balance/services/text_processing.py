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
    Serviço responsável por processar textos e dados extraídos, interpretar linguagem natural,
    e decidir a rota apropriada com base em categorias, incluindo finanças e outros temas.
    """

    def __init__(self):
        # Palavras-chave financeiras ampliadas
        self.financial_keywords = [
            "finança",
            "investimento",
            "dinheiro",
            "ações",
            "economia",
            "receita",
            "lucro",
            "imposto",
            "taxa",
            "ROI",
            "juros",
            "rentabilidade",
            "poupança",
            "despesa",
            "dividendos",
            "cash flow",
            "custo",
            "orçamento",
            "rentabilidade",
            "análise",
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
        Analisa o texto usando spaCy e Transformers, incluindo palavras-chave e entidades.
        """
        try:
            doc = nlp(text)
            sentiment = classifier(text)

            keywords = [token.text for token in doc]
            entities = [(ent.text, ent.label_) for ent in doc.ents]

            # Verifica se há termos financeiros nas entidades nomeadas
            if (
                not any(token in self.financial_keywords for token in keywords)
                and entities
            ):
                # Se houver entidades financeiras, marca como financeiro
                keywords += ["finance"]

            return {
                "keywords": keywords,
                "sentiment": sentiment[0]["label"],
                "entities": entities,
            }
        except Exception as e:
            logging.error(f"Erro ao analisar o texto: {str(e)}")
            return {
                "keywords": ["generico"],
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
        Aqui também é onde identificamos qual serviço financeiro usar, dependendo do conteúdo.
        """
        keywords = analysis.get("keywords", [])
        entities = analysis.get("entities", [])

        # Verifica se é um tópico financeiro
        if any(keyword in self.financial_keywords for keyword in keywords):
            # Identificar qual serviço financeiro usar
            if "ROI" in keywords or "retorno" in keywords:
                return "advanced_financial_analysis"  # Direciona para análise avançada
            elif any(
                term in ["despesa", "orçamento", "lucro", "custo"] for term in keywords
            ):
                return "financial_analysis"  # Direciona para análise prática
            else:
                return "general_financial"  # Rota geral para outros tópicos financeiros

        # Verifica se é um tópico de piada
        elif any(keyword in self.joke_keywords for keyword in keywords):
            return "joke"

        elif "generico" in keywords:
            return "generic"  # Rota para perguntas genéricas

        else:
            return "general"  # Rota para tópicos gerais

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
