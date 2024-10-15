from typing import List, Dict


class TheoreticalFinancialAnalysisService:
    """
    Serviço responsável por fornecer explicações teóricas sobre conceitos e estratégias financeiras,
    permitindo ao usuário um entendimento completo dos termos e métodos aplicados em análises financeiras.
    """

    def __init__(self):
        self.finance_concepts = {
            "ROI": "O Retorno sobre o Investimento (ROI) é uma métrica usada para avaliar a eficiência de um investimento. Ele é calculado pela fórmula: (Lucro Líquido / Custo do Investimento) * 100.",
            "Payback": "O Período de Payback é o tempo necessário para recuperar o valor investido em um projeto ou investimento.",
            "Margem de Contribuição": "A Margem de Contribuição é a diferença entre a receita de vendas e os custos variáveis, usada para cobrir custos fixos e gerar lucro.",
            "Ponto de Equilíbrio": "O Ponto de Equilíbrio é o nível de vendas em que a receita total iguala os custos totais, resultando em lucro zero.",
            "Juros Compostos": "Os Juros Compostos referem-se ao cálculo de juros sobre o montante inicial, além dos juros acumulados de períodos anteriores.",
        }

    def explain_financial_concept(self, concept: str) -> str:
        """
        Explica um conceito financeiro teórico com base na solicitação do usuário.

        Args:
            concept (str): O conceito financeiro solicitado.

        Returns:
            str: Explicação detalhada do conceito.
        """
        return self.finance_concepts.get(
            concept, "Desculpe, o conceito solicitado não foi encontrado."
        )

    def list_available_concepts(self) -> List[str]:
        """
        Lista todos os conceitos financeiros disponíveis para explicação.

        Returns:
            List[str]: Lista de conceitos financeiros.
        """
        return list(self.finance_concepts.keys())

    def suggest_investment_strategies(self) -> str:
        """
        Sugere estratégias de investimento com base em diferentes perfis de investidor.

        Returns:
            str: Sugestões de estratégias de investimento.
        """
        return (
            "1. **Perfil Conservador**: Opte por investimentos de baixo risco, como títulos de renda fixa ou CDBs.\n"
            "2. **Perfil Moderado**: Considere uma combinação de renda fixa com ações de empresas sólidas e fundos imobiliários.\n"
            "3. **Perfil Agressivo**: Ações de crescimento, criptomoedas e startups podem proporcionar maiores retornos, mas com risco elevado.\n"
        )

    def generate_theoretical_report(self, conceitos_solicitados: List[str]) -> str:
        """
        Gera um relatório teórico detalhado explicando todos os conceitos financeiros solicitados.

        Args:
            conceitos_solicitados (List[str]): Lista de conceitos financeiros que o usuário deseja aprender.

        Returns:
            str: Relatório teórico detalhado.
        """
        report = "📚 **Relatório Teórico Financeiro**\n\n"
        for conceito in conceitos_solicitados:
            explicacao = self.explain_financial_concept(conceito)
            report += f"**{conceito}**:\n{explicacao}\n\n"
        return report
