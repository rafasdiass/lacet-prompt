class GreetingService:
    def __init__(self, catelina_lacet):
        self.catelina_lacet = catelina_lacet

    def get_greeting_response(self, sentiment: str) -> str:
        """
        Retorna uma saudação personalizada com base no sentimento do prompt.
        """
        if sentiment == 'POSITIVE':
            return f"Olá! Estou aqui para te ajudar! {self.catelina_lacet.tipo_humor.capitalize()} como sempre!"
        elif sentiment == 'NEGATIVE':
            return f"Ei, não se preocupe! Vamos superar isso. Estou aqui para te apoiar."
        else:
            return f"Oi! Como posso ajudar? Estou pronta para tudo."
