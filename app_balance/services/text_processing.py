from textblob import TextBlob, exceptions

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

    def analyze_sentiment(self, prompt: str) -> str:
        """
        Usa TextBlob para analisar o sentimento do prompt.
        """
        try:
            blob = TextBlob(prompt)
            sentiment_polarity = blob.sentiment.polarity

            if sentiment_polarity > 0:
                return 'POSITIVE'
            elif sentiment_polarity < 0:
                return 'NEGATIVE'
            else:
                return 'NEUTRAL'
        except exceptions.MissingCorpusError:
            return 'NEUTRAL'
