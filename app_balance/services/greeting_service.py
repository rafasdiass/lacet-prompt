class GreetingService:
    def __init__(self):
        # Não requer nenhum parâmetro externo
        pass

    def is_greeting(self, prompt: str) -> bool:
        """
        Verifica se o prompt é uma saudação simples.
        """
        greetings = ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'hello', 'hi']
        return any(greet in prompt.lower() for greet in greetings)

    def get_greeting_response(self, sentiment: str) -> str:
        """
        Retorna uma resposta apropriada para a saudação com base no sentimento.
        """
        if sentiment == 'POSITIVE':
            return "Olá! Que bom te ver animado! Como posso te ajudar?"
        elif sentiment == 'NEGATIVE':
            return "Oi, parece que você não está em um ótimo dia. Como posso ajudar a melhorar?"
        else:
            return "Olá! Como posso te ajudar hoje?"
