from app_balance.services.openai_service import analyze_data

class GPTService:
    """
    Serviço para gerenciar a comunicação com o GPT-4.
    A responsabilidade do fallback e da lógica de interação está na IA.
    """

    def enviar_prompt(self, prompt: str) -> str:
        """
        Envia um prompt para o GPT-4.
        """
        return analyze_data(prompt)
