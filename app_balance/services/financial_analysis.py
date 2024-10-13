# app_balance/services/financial_analysis.py
from typing import Dict

class FinancialAnalysisService:
    """
    Serviço para realizar uma análise financeira detalhada com base nos dados de custos, receita e categorias.
    Inclui cálculos de margem de contribuição, ponto de equilíbrio, ROI, payback e sensibilidade.
    """

    def gerar_analise_detalhada(self, custos: Dict, receita_projetada: float, valor_hora: float, categorias_custos: Dict) -> str:
        """
        Gera uma análise financeira detalhada, abrangendo margem de contribuição, ROI, ponto de equilíbrio, e outros.

        Args:
            custos (dict): Dicionário com os custos totais.
            receita_projetada (float): Receita estimada para o período.
            valor_hora (float): Valor estimado da hora trabalhada.
            categorias_custos (dict): Custos detalhados por categoria.

        Returns:
            str: O relatório detalhado da análise financeira.
        """
        # 1. Cálculo do lucro estimado
        total_custos = custos['total_custos']
        lucro_estimado = receita_projetada - total_custos
        margem_lucro_real = (lucro_estimado / receita_projetada) * 100 if receita_projetada > 0 else 0

        # 2. Margem de Contribuição (desconsidera custos fixos, focando em custos variáveis)
        custos_variaveis = sum([valor for categoria, valor in categorias_custos.items() if categoria.lower() != 'fixos'])
        margem_contribuicao = receita_projetada - custos_variaveis
        margem_contribuicao_percentual = (margem_contribuicao / receita_projetada) * 100 if receita_projetada > 0 else 0

        # 3. Ponto de Equilíbrio (Break-even)
        custos_fixos = categorias_custos.get('fixos', 0)
        if margem_contribuicao_percentual > 0:
            ponto_equilibrio = custos_fixos / (margem_contribuicao_percentual / 100)
        else:
            ponto_equilibrio = 0

        # 4. Retorno sobre o Investimento (ROI)
        investimentos = custos.get('investimentos', 0)
        if investimentos > 0:
            roi = (lucro_estimado / investimentos) * 100
        else:
            roi = 0

        # 5. Payback (tempo necessário para recuperar o investimento)
        if margem_contribuicao > 0:
            payback = investimentos / margem_contribuicao if investimentos > 0 else 0
        else:
            payback = 0

        # 6. Análise de Sensibilidade (como variações afetam o lucro)
        variacao_receita_positiva = receita_projetada * 1.1  # 10% de aumento na receita
        lucro_com_variacao_positiva = variacao_receita_positiva - total_custos
        margem_lucro_variacao_positiva = (lucro_com_variacao_positiva / variacao_receita_positiva) * 100

        variacao_receita_negativa = receita_projetada * 0.9  # 10% de redução na receita
        lucro_com_variacao_negativa = variacao_receita_negativa - total_custos
        margem_lucro_variacao_negativa = (lucro_com_variacao_negativa / variacao_receita_negativa) * 100

        # 7. Detalhamento de custos por categoria
        categorias_detalhadas = "\n".join([f"- {categoria}: R$ {valor:.2f}" for categoria, valor in categorias_custos.items()])

        # Geração do relatório detalhado
        return (
            f"📊 Análise Financeira Detalhada:\n\n"
            f"1. **Lucro Estimado**:\n"
            f"   - Receita projetada: R$ {receita_projetada:.2f}\n"
            f"   - Total de custos: R$ {total_custos:.2f}\n"
            f"   - Lucro estimado: R$ {lucro_estimado:.2f}\n"
            f"   - Margem de lucro real: {margem_lucro_real:.2f}%\n\n"
            
            f"2. **Margem de Contribuição**:\n"
            f"   - Custos Variáveis: R$ {custos_variaveis:.2f}\n"
            f"   - Margem de contribuição: R$ {margem_contribuicao:.2f} ({margem_contribuicao_percentual:.2f}%)\n\n"
            
            f"3. **Ponto de Equilíbrio (Break-even)**:\n"
            f"   - Ponto de equilíbrio: R$ {ponto_equilibrio:.2f}\n\n"
            
            f"4. **Retorno sobre o Investimento (ROI)**:\n"
            f"   - Investimentos: R$ {investimentos:.2f}\n"
            f"   - ROI: {roi:.2f}%\n\n"
            
            f"5. **Payback**:\n"
            f"   - Payback: {payback:.2f} meses\n\n"
            
            f"6. **Análise de Sensibilidade**:\n"
            f"   - Aumento de 10% na receita: Margem de lucro {margem_lucro_variacao_positiva:.2f}%\n"
            f"   - Redução de 10% na receita: Margem de lucro {margem_lucro_variacao_negativa:.2f}%\n\n"
            
            f"7. **Detalhamento de Custos por Categoria**:\n{categorias_detalhadas}\n"
        )
