from textblob import TextBlob, exceptions
import datetime
import re
import nltk

# Baixar o recurso necessário para o TextBlob
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

class TextProcessingService:
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
        greetings = ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite']
        return any(greet in prompt for greet in greetings)

    def is_finance_related(self, prompt: str) -> bool:
        """
        Verifica se o prompt está relacionado a finanças, usando palavras-chave e padrões de frases comuns.
        """
        finance_keywords = ['finança', 'dinheiro', 'investimento', 'gastos', 'receita', 'saldo', 'orçamento', 'despesa']
        # Verifica se há alguma palavra-chave financeira
        if any(keyword in prompt for keyword in finance_keywords):
            return True
        # Verifica padrões comuns relacionados a perguntas sobre dinheiro
        finance_patterns = [
            r'quanto.*dinheiro', 
            r'como.*poupar', 
            r'qual.*melhor.*investimento'
        ]
        return any(re.search(pattern, prompt) for pattern in finance_patterns)

    def is_time_related(self, prompt: str) -> bool:
        """
        Verifica se o prompt está relacionado a tempo ou horário, usando palavras-chave e padrões de frases comuns.
        """
        time_keywords = ['hora', 'que horas', 'data', 'hoje', 'amanhã', 'ontem']
        if any(keyword in prompt for keyword in time_keywords):
            return True
        # Padrões comuns relacionados ao tempo
        time_patterns = [
            r'qual.*data', 
            r'quando.*evento', 
            r'que horas'
        ]
        return any(re.search(pattern, prompt) for pattern in time_patterns)

    def analyze_text(self, prompt: str) -> dict:
        """
        Usa TextBlob e nltk para analisar o texto do prompt, retornando informações sobre tópicos, palavras-chave e sentimento.
        """
        try:
            blob = TextBlob(prompt)
            noun_phrases = blob.noun_phrases  # Frases nominais que podem conter tópicos importantes
            sentiment_polarity = blob.sentiment.polarity  # Análise de sentimento
            keywords = list(set(noun_phrases))  # Extrair tópicos e palavras-chave identificadas no texto

            # Usar nltk para identificar as classes gramaticais (part-of-speech tagging)
            tokens = nltk.word_tokenize(prompt)
            pos_tags = nltk.pos_tag(tokens)  # Classificação das palavras (adjetivo, substantivo, verbo etc.)

            return {
                'keywords': keywords,
                'sentiment': 'POSITIVE' if sentiment_polarity > 0 else 'NEGATIVE' if sentiment_polarity < 0 else 'NEUTRAL',
                'is_finance_related': self.is_finance_related(prompt),
                'is_time_related': self.is_time_related(prompt),
                'pos_tags': pos_tags  # Lista de palavras classificadas gramaticalmente
            }
        except exceptions.MissingCorpusError:
            return {
                'keywords': [],
                'sentiment': 'NEUTRAL',
                'is_finance_related': False,
                'is_time_related': False,
                'pos_tags': []
            }
        except Exception as e:
            return {
                'keywords': [],
                'sentiment': 'NEUTRAL',
                'is_finance_related': False,
                'is_time_related': False,
                'pos_tags': [],
                'error': str(e)
            }

    def handle_general_query(self, prompt: str) -> dict:
        """
        Analisa o prompt e gera um dicionário de análise apropriado.
        """
        cleaned_prompt = self.clean_prompt(prompt)
        return self.analyze_text(cleaned_prompt)
