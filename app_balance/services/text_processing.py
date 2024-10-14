from textblob import TextBlob, exceptions
import datetime
import re
import nltk

# Baixar o recurso necessário para o TextBlob
nltk.download('punkt')
class TextProcessingService:
    def clean_prompt(self, prompt: str) -> str:
        """
        Limpa o prompt removendo espaços extras e convertendo para minúsculas.
        """
        return prompt.strip().lower()

    def is_greeting(self, prompt: str) -> bool:
        """
        Verifica se o prompt é uma saudação simples.
        """
        greetings = ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite']
        return any(greet in prompt for greet in greetings)

    def is_finance_related(self, prompt: str) -> bool:
        """
        Verifica se o prompt está relacionado a finanças.
        """
        finance_keywords = ['finança', 'dinheiro', 'investimento', 'gastos', 'receita', 'saldo', 'orçamento', 'despesa']
        return any(keyword in prompt for keyword in finance_keywords)

    def is_time_related(self, prompt: str) -> bool:
        """
        Verifica se o prompt está relacionado a tempo ou horário.
        """
        time_keywords = ['hora', 'que horas', 'data', 'hoje', 'amanhã', 'ontem']
        return any(keyword in prompt for keyword in time_keywords)

    def analyze_text(self, prompt: str) -> dict:
        """
        Usa TextBlob para analisar o texto do prompt, retornando informações sobre tópicos, palavras-chave e sentimento.
        """
        try:
            blob = TextBlob(prompt)
            noun_phrases = blob.noun_phrases
            sentiment_polarity = blob.sentiment.polarity
            keywords = list(set(noun_phrases))  # Extrair tópicos e palavras-chave identificadas no texto

            return {
                'keywords': keywords,
                'sentiment': 'POSITIVE' if sentiment_polarity > 0 else 'NEGATIVE' if sentiment_polarity < 0 else 'NEUTRAL',
                'is_finance_related': self.is_finance_related(prompt),
                'is_time_related': self.is_time_related(prompt)
            }
        except exceptions.MissingCorpusError:
            return {
                'keywords': [],
                'sentiment': 'NEUTRAL',
                'is_finance_related': False,
                'is_time_related': False
            }
        except Exception as e:
            return {
                'keywords': [],
                'sentiment': 'NEUTRAL',
                'is_finance_related': False,
                'is_time_related': False,
                'error': str(e)
            }

    def handle_general_query(self, prompt: str) -> dict:
        """
        Analisa o prompt e gera um dicionário de análise apropriado.
        """
        cleaned_prompt = self.clean_prompt(prompt)
        return self.analyze_text(cleaned_prompt)
