import spacy
from textblob import TextBlob, exceptions
import nltk
import re
from transformers import pipeline

# Baixar o recurso necessário para o TextBlob e nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Carregar o modelo de linguagem do spacy (en_core_web_sm é o modelo de inglês, você pode mudar se necessário)
nlp = spacy.load("en_core_web_sm")

class TextProcessingService:
    def __init__(self):
        # Inicializa o pipeline do transformers para perguntas e respostas gerais
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

    def clean_prompt(self, prompt: str) -> str:
        """
        Limpa o prompt removendo espaços extras e convertendo para minúsculas.
        Remove também caracteres especiais e números.
        """
        prompt = re.sub(r'[^a-zA-Z\s]', '', prompt)  # Remove caracteres especiais e números
        return prompt.strip().lower()

    def is_greeting(self, prompt: str) -> bool:
        """
        Verifica se o prompt é uma saudação simples.
        """
        greetings = ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'hello', 'hi']
        return any(greet in prompt.lower() for greet in greetings)

    def analyze_text(self, prompt: str) -> dict:
        """
        Usa TextBlob e spacy para analisar o texto do prompt, retornando informações sobre tópicos, entidades e sentimento.
        """
        try:
            # Processamento com TextBlob para análise de sentimento e extração de palavras-chave
            blob = TextBlob(prompt)
            noun_phrases = blob.noun_phrases  # Frases nominais que podem conter tópicos importantes
            sentiment_polarity = blob.sentiment.polarity  # Análise de sentimento

            # Processamento com spacy para análise gramatical e entidades nomeadas
            doc = nlp(prompt)
            entities = [(ent.text, ent.label_) for ent in doc.ents]  # Extração de entidades nomeadas
            pos_tags = [(token.text, token.pos_) for token in doc]  # Classificação gramatical (adjetivo, substantivo, etc.)

            return {
                'keywords': list(set(noun_phrases)),  # Tópicos identificados
                'sentiment': 'POSITIVE' if sentiment_polarity > 0 else 'NEGATIVE' if sentiment_polarity < 0 else 'NEUTRAL',
                'entities': entities,  # Entidades nomeadas
                'pos_tags': pos_tags  # Lista de palavras classificadas gramaticalmente
            }
        except exceptions.MissingCorpusError:
            return {
                'keywords': [],
                'sentiment': 'NEUTRAL',
                'entities': [],
                'pos_tags': []
            }
        except Exception as e:
            return {
                'keywords': [],
                'sentiment': 'NEUTRAL',
                'entities': [],
                'pos_tags': [],
                'error': str(e)
            }

    def process_prompt(self, prompt: str) -> dict:
        """
        Processa o prompt e retorna uma análise detalhada com keywords, sentimento, entidades e POS tags.
        """
        cleaned_prompt = self.clean_prompt(prompt)
        return self.analyze_text(cleaned_prompt)

    def answer_with_transformers(self, prompt: str) -> str:
        """
        Usa o transformers para responder a perguntas gerais com base em conhecimento amplo.
        """
        context = """
        Sou uma IA com vasto conhecimento em finanças, cultura pop, ciência e muito mais. 
        Posso te ajudar com temas variados, desde orçamento pessoal até curiosidades sobre filmes e séries.
        """
        result = self.qa_pipeline(question=prompt, context=context)
        return result['answer']
