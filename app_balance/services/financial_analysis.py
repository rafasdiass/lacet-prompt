from typing import Dict

class FinancialAnalysisService:
    """
    Serviço para realizar uma análise financeira detalhada com base nos custos, receita e categorias,
    incluindo impostos, taxas, juros compostos e análise de sensibilidade.
    """

    def calcular_valor_hora(self, total_custos: float, horas_trabalhadas: float) -> float:
        """
        Calcula o valor da hora trabalhada com base no total de custos e horas trabalhadas.

        Args:
            total_custos (float): O custo total.
            horas_trabalhadas (float): Total de horas trabalhadas no período.

        Returns:
            float: O valor da hora trabalhada.
        """
        if horas_trabalhadas == 0:
            raise ValueError("Horas trabalhadas não pode ser zero.")
        return total_custos / horas_trabalhadas

    def gerar_analise_detalhada(self, custos: Dict, receita_projetada: float, horas_trabalhadas: float, categorias_custos: Dict, 
                                taxa_imposto: float = 0.15, taxa_juros: float = 0.05) -> str:
        """
        Gera uma análise financeira detalhada, abrangendo margem de contribuição, ROI, ponto de equilíbrio,
        payback, impostos, taxas e sensibilidade.

        Args:
            custos (dict): Dicionário com os custos totais.
            receita_projetada (float): Receita estimada para o período.
            horas_trabalhadas (float): Total de horas trabalhadas no período.
            categorias_custos (dict): Custos detalhados por categoria.
            taxa_imposto (float): Percentual de imposto sobre o lucro.
            taxa_juros (float): Taxa de juros para cálculo de sensibilidade.

        Returns:
            str: O relatório detalhado da análise financeira.
        """
        total_custos = custos['total_custos']
        lucro_estimado = receita_projetada - total_custos
        lucro_apos_impostos = lucro_estimado * (1 - taxa_imposto)
        margem_lucro_real = (lucro_apos_impostos / receita_projetada) * 100 if receita_projetada > 0 else 0

        # Calcular o valor da hora trabalhada
        valor_hora = self.calcular_valor_hora(total_custos, horas_trabalhadas)

        # Margem de Contribuição
        custos_variaveis = sum([v for cat, v in categorias_custos.items() if cat.lower() != 'fixos'])
        margem_contribuicao = receita_projetada - custos_variaveis
        margem_contribuicao_percentual = (margem_contribuicao / receita_projetada) * 100 if receita_projetada > 0 else 0

        # Ponto de Equilíbrio (Break-even)
        custos_fixos = categorias_custos.get('fixos', 0)
        ponto_equilibrio = custos_fixos / (margem_contribuicao_percentual / 100) if margem_contribuicao_percentual > 0 else 0

        # ROI e Payback
        investimentos = custos.get('investimentos', 0)
        roi = (lucro_apos_impostos / investimentos) * 100 if investimentos > 0 else 0
        payback = investimentos / margem_contribuicao if margem_contribuicao > 0 else 0

        # Simulação de investimento (pode usar um serviço avançado para esse cálculo, se disponível)
        # Para fins de exemplo, mantemos o campo comentado.
        # investimento_simulado = self.advanced_financial_service.simulate_investment(10000, market_data, taxa_imposto)

        # Juros Compostos e Sensibilidade
        variacao_receita_positiva = receita_projetada * (1 + taxa_juros)
        lucro_com_variacao_positiva = variacao_receita_positiva - total_custos
        margem_lucro_variacao_positiva = (lucro_com_variacao_positiva / variacao_receita_positiva) * 100

        variacao_receita_negativa = receita_projetada * (1 - taxa_juros)
        lucro_com_variacao_negativa = variacao_receita_negativa - total_custos
        margem_lucro_variacao_negativa = (lucro_com_variacao_negativa / variacao_receita_negativa) * 100

        # Geração do relatório final
        return (
            f"📊 **Análise Financeira Completa**:\n\n"
            f"1. **Lucro Estimado**:\n"
            f"   - Receita projetada: R$ {receita_projetada:.2f}\n"
            f"   - Total de custos: R$ {total_custos:.2f}\n"
            f"   - Lucro após impostos: R$ {lucro_apos_impostos:.2f}\n"
            f"   - Margem de lucro real: {margem_lucro_real:.2f}%\n\n"

            f"2. **Margem de Contribuição**:\n"
            f"   - Custos Variáveis: R$ {custos_variaveis:.2f}\n"
            f"   - Margem de contribuição: R$ {margem_contribuicao:.2f} ({margem_contribuicao_percentual:.2f}%)\n\n"
            
            f"3. **Ponto de Equilíbrio (Break-even)**:\n"
            f"   - Ponto de equilíbrio: R$ {ponto_equilibrio:.2f}\n\n"

            f"4. **Valor da Hora Trabalhada**:\n"
            f"   - Total de horas trabalhadas: {horas_trabalhadas}\n"
            f"   - Valor da hora: R$ {valor_hora:.2f}\n\n"
            
            f"5. **Retorno sobre o Investimento (ROI)**:\n"
            f"   - Investimentos: R$ {investimentos:.2f}\n"
            f"   - ROI: {roi:.2f}%\n\n"
            
            f"6. **Payback**:\n"
            f"   - Payback: {payback:.2f} meses\n\n"

            f"7. **Análise de Sensibilidade**:\n"
            f"   - Aumento de 5% na receita: Margem de lucro {margem_lucro_variacao_positiva:.2f}%\n"
            f"   - Redução de 5% na receita: Margem de lucro {margem_lucro_variacao_negativa:.2f}%\n\n"
        )
