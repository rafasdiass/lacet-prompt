import spacy
from transformers import pipeline
import logging
from typing import Dict, List, Tuple, Any, Union

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Carregar modelo do spaCy e Transformers
nlp = spacy.load("en_core_web_sm")

# Definindo o pipeline com o modelo RoBERTa para análise de sentimentos
classifier = pipeline("sentiment-analysis", model="roberta-base")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


class TextProcessingService:
    """
    Serviço responsável por processar textos e dados extraídos, interpretar linguagem natural,
    e decidir a rota apropriada com base em categorias, incluindo finanças e outros temas.
    Também inclui funcionalidade de summarization para resumir textos longos.
    """

    def __init__(self):
        # Palavras-chave financeiras ampliadas
        self.financial_keywords: List[str] = [
            "finança", "investimento", "dinheiro", "ações", "economia", "receita", 
            "lucro", "imposto", "taxa", "ROI", "juros", "rentabilidade", "poupança", 
            "despesa", "dividendos", "cash flow", "custo", "orçamento", "análise",
        ]
        self.joke_keywords: List[str] = ["piada", "engraçado", "brincadeira"]

    def clean_text(self, text: str) -> str:
        """
        Limpa o texto removendo caracteres especiais e números.
        """
        import re
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        return text.strip().lower()

    def analyze_text(self, text: str) -> Dict[str, Union[str, List[Tuple[str, str]], List[str]]]:
        """
        Analisa o texto usando spaCy e Transformers, incluindo palavras-chave e entidades.
        Usa modelos baseados em contexto para compreender o sentido geral das frases.
        """
        try:
            logging.info(f"Analisando texto: {text}")
            doc = nlp(text)
            sentiment = classifier(text)

            # Captura as palavras do texto e suas entidades
            keywords: List[str] = [token.text for token in doc]
            entities: List[Tuple[str, str]] = [(ent.text, ent.label_) for ent in doc.ents]

            # Refatoração da lógica com 'any' para melhorar a legibilidade
            if any(token in self.financial_keywords for token in keywords) or entities:
                keywords.append("finance")

            logging.info(f"Palavras-chave detectadas: {keywords}")
            logging.info(f"Entidades detectadas: {entities}")
            logging.info(f"Sentimento detectado: {sentiment}")

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

    def summarize_text(self, text: str) -> str:
        """
        Fornece um resumo do texto fornecido usando o modelo de Summarization.
        """
        try:
            summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            logging.error(f"Erro ao resumir o texto: {str(e)}")
            return "Erro ao gerar resumo."

    def process_data_from_file(self, data: Dict[str, Any]) -> Dict[str, Union[str, List[Tuple[str, str]], List[str]]]:
        """
        Processa os dados extraídos de arquivos e os converte para um formato adequado para análise de texto.
        """
        text_representation = " ".join(
            [f"{cat} {val}" for cat, val in data.get("categorias_custos", {}).items()]
        )
        return self.analyze_text(text_representation)

    def decide_route(self, analysis: Dict[str, Union[str, List[Tuple[str, str]], List[str]]]) -> str:
        """
        Decide a rota com base na análise do texto ou dados.
        Aqui também é onde identificamos qual serviço financeiro usar, dependendo do conteúdo.
        """
        keywords = analysis.get("keywords", [])
        entities = analysis.get("entities", [])

        logging.info(f"Decidindo a rota com base nas palavras-chave: {keywords}")

        # Verifica se é um tópico financeiro
        if any(keyword in self.financial_keywords for keyword in keywords):
            if "ROI" in keywords or "retorno" in keywords:
                return "advanced_financial_analysis"  # Direciona para análise avançada
            elif any(term in ["despesa", "orçamento", "lucro", "custo"] for term in keywords):
                return "financial_analysis"  # Direciona para análise prática
            else:
                return "general_financial"  # Rota geral para outros tópicos financeiros

        # Verifica se é um tópico de piada
        elif any(keyword in self.joke_keywords for keyword in keywords):
            return "joke"

        elif "generico" in keywords:
            return "generic"  # Rota para perguntas genéricas

        return "general"  # Rota para tópicos gerais

    def route_and_process(self, input_data: Union[str, Dict[str, Any]], is_summary: bool = False) -> str:
        """
        Processa tanto textos fornecidos diretamente pelo input do usuário quanto dados extraídos de arquivos.
        Adiciona a opção de realizar a ação de Summarization quando o parâmetro is_summary for True.
        """
        if isinstance(input_data, str):
            cleaned_text = self.clean_text(input_data)
            analysis = self.analyze_text(cleaned_text)

            # Resumo se o parâmetro for solicitado
            if is_summary:
                return self.summarize_text(cleaned_text)

        else:
            analysis = self.process_data_from_file(input_data)

        # Decide a rota com base na análise
        route = self.decide_route(analysis)
        logging.info(f"Rota decidida: {route}")
        return route
