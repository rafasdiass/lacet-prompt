from app_balance.services.openai_service import analyze_data

class GPTService:
    """
    Serviço para gerenciar a comunicação com o GPT-4, enviando prompts e recebendo respostas.
    Este serviço é focado apenas na comunicação com a OpenAI.
    """

    def enviar_prompt(self, prompt: str) -> str:
        """
        Envia um prompt para o GPT-4 e retorna a resposta.
        Se falhar por exceder cota, retorna uma resposta simulada.

        Args:
            prompt (str): O prompt a ser enviado.

        Returns:
            str: A resposta do GPT-4.
        """
        return analyze_data(prompt)

    def gerar_prompt_recebimentos(self, recebimentos: list) -> str:
        """
        Gera um prompt detalhado com base nos recebimentos extraídos para análise via GPT-4.

        Args:
            recebimentos (list): Lista de objetos Recebimento contendo dados de recebimentos.

        Returns:
            str: Prompt formatado para enviar ao GPT-4.
        """
        total_recebimentos = sum([r.valor for r in recebimentos])
        detalhes_recebimentos = "\n".join([f"Recebimento em {r.data}: R$ {r.valor:.2f}" for r in recebimentos])

        prompt = (
            f"Você recebeu os seguintes recebimentos ao longo do mês:\n{detalhes_recebimentos}\n\n"
            f"O total de recebimentos foi de R$ {total_recebimentos:.2f}.\n"
            "Por favor, forneça uma análise detalhada desses recebimentos, incluindo sugestões sobre como melhor gerenciá-los."
        )

        return prompt
