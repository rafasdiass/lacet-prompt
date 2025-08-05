<<<<<<< HEAD
import spacy
import logging
from transformers import pipeline
from typing import Dict, Union
from services.gpt_service import GPTService

# Carregar o modelo spaCy para fallback local
nlp = spacy.load("en_core_web_sm")
=======
import openai
import logging
import re
from environs import Env

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Carregar variáveis de ambiente
env = Env()
env.read_env()


# Configurações da API OpenAI
openai_key = env.str("OPENAI_API_KEY", default=None)
organization_id = env.str("OPENAI_ORG_ID", default=None)

# Verifica se as credenciais da API OpenAI estão definidas
if not openai_key:
    raise EnvironmentError("A chave da API do OpenAI não está definida. Verifique o arquivo .env")
if not organization_id:
    raise EnvironmentError("O ID da organização do OpenAI não está definido. Verifique o arquivo .env")

# Inicializa o cliente OpenAI
openai.api_key = openai_key
>>>>>>> main

# Definir pipeline local de fallback (Roberta para análise de sentimentos)
classifier = pipeline("sentiment-analysis", model="roberta-base")

class TextProcessingService:
    """
    Serviço responsável por enviar o prompt diretamente ao GPT-4,
    e usar análise local como fallback em caso de falha.
    """

<<<<<<< HEAD
    def __init__(self, gpt_service: GPTService):
        self.gpt_service = gpt_service  # Sempre utilizará o serviço GPT-4
=======
    def __init__(self):
        # Palavras-chave financeiras ampliadas
        self.financial_keywords = [
            "finança", "investimento", "dinheiro", "ações", "economia", "receita",
            "lucro", "imposto", "taxa", "ROI", "juros", "rentabilidade", "poupança",
            "despesa", "dividendos", "cash flow", "custo", "orçamento", "análise"
        ]
        self.joke_keywords = ["piada", "engraçado", "brincadeira"]
>>>>>>> main

    def clean_text(self, text: str) -> str:
        """
        Limpa o texto removendo caracteres especiais e números.
        """
<<<<<<< HEAD
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

=======
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        return text.strip().lower()

    def analyze_text(self, text: str) -> dict:
        """
        Analisa o texto usando GPT-4 via OpenAI API. Em caso de falha, retorna uma análise neutra.
        """
        try:
            # Usando a API GPT-4 para análise de texto
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": text}],
                max_tokens=500,
                temperature=0.7
            )
            analysis_text = response.choices[0].message['content'].strip()

            keywords = self.extract_keywords(analysis_text)
            sentiment = self.extract_sentiment(analysis_text)

            logging.info("Análise feita com GPT-4.")
>>>>>>> main
            return {
                "keywords": keywords,
                "sentiment": sentiment,
                "entities": []  # Placeholder, sem uso de entidades
            }

        except Exception as e:
<<<<<<< HEAD
            logging.error(f"Erro ao analisar texto localmente: {str(e)}")
            return {"keywords": ["generico"], "sentiment": "NEUTRAL", "entities": []}

    def process_text(self, input_data: str) -> str:
=======
            logging.error(f"Erro na API do OpenAI. Retornando análise neutra. Erro: {str(e)}")
            # Fallback simples: retorna resultado neutro
            return {
                "keywords": ["generico"],
                "sentiment": "NEUTRAL",
                "entities": []
            }

    def extract_keywords(self, analysis_text: str) -> list:
        """
        Extrai as palavras-chave da resposta gerada pelo GPT-4.
        """
        # Supomos que o GPT-4 lista palavras-chave em algum formato
        keyword_line = [line for line in analysis_text.split("\n") if "Palavras-chave" in line]
        if keyword_line:
            return keyword_line[0].replace("Palavras-chave:", "").strip().split(", ")
        return []

    def extract_sentiment(self, analysis_text: str) -> str:
        """
        Extrai a classificação de sentimento da resposta gerada pelo GPT-4.
        """
        if "positivo" in analysis_text.lower():
            return "POSITIVE"
        elif "negativo" in analysis_text.lower():
            return "NEGATIVE"
        else:
            return "NEUTRAL"

    def process_data_from_file(self, data: dict) -> dict:
>>>>>>> main
        """
        Processa o texto fornecido e sempre tenta enviar primeiro para o GPT-4.
        Se falhar, faz o fallback para análise local.
        """
        cleaned_text = self.clean_text(input_data)

<<<<<<< HEAD
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
=======
    def decide_route(self, analysis: dict) -> str:
        """
        Decide a rota com base na análise do texto ou dados.
        Aqui também é onde identificamos qual serviço financeiro usar, dependendo do conteúdo.
        """
        keywords = analysis.get("keywords", [])

        # Verifica se é um tópico financeiro
        if any(keyword in self.financial_keywords for keyword in keywords):
            if "ROI" in keywords or "retorno" in keywords:
                return "advanced_financial_analysis"
            elif any(term in ["despesa", "orçamento", "lucro", "custo"] for term in keywords):
                return "financial_analysis"
            else:
                return "general_financial"

        # Verifica se é um tópico de piada
        elif any(keyword in self.joke_keywords for keyword in keywords):
            return "joke"

        elif "generico" in keywords:
            return "generic"

        else:
            return "general"

    def route_and_process(self, input_data: dict) -> str:
        """
        Processa tanto textos fornecidos diretamente pelo input do usuário quanto dados extraídos de arquivos.
        """
        if isinstance(input_data, str):
            cleaned_text = self.clean_text(input_data)
            analysis = self.analyze_text(cleaned_text)
        else:
            analysis = self.process_data_from_file(input_data)

        route = self.decide_route(analysis)
        logging.info(f"Rota decidida: {route}")
        return route
>>>>>>> main
