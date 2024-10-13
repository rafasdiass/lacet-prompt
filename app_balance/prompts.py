from typing import Dict, List

class PromptService:
    """
    Serviço para gerar prompts detalhados para análise financeira e outras interações com a IA.
    """

    def gerar_prompt_analise(self, custos: Dict, valor_hora: float, categorias_custos: Dict, margem_lucro_desejada: float, receita_projetada: float) -> str:
        """
        Gera um prompt detalhado para análise dos custos reais, valor da hora trabalhada e estimativas financeiras.

        Args:
            custos (dict): Dicionário com os custos totais.
            valor_hora (float): Valor calculado da hora trabalhada.
            categorias_custos (dict): Dicionário com custos detalhados por categoria.
            margem_lucro_desejada (float): Margem de lucro desejada em porcentagem.
            receita_projetada (float): Receita estimada para o período em análise.

        Returns:
            str: O prompt gerado.
        """
        return (
            f"Análise financeira:\n"
            f"Total de custos: R$ {custos['total_custos']:.2f}\n"
            f"Valor da hora: R$ {valor_hora:.2f}\n"
            f"Receita projetada: R$ {receita_projetada:.2f}\n"
            f"Margem de lucro desejada: {margem_lucro_desejada}%\n"
            f"\nCategorias de custos:\n" + "\n".join([f"{k}: R$ {v}" for k, v in categorias_custos.items()])
        )
