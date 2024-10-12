# -*- coding: utf-8 -*-
"""Serviço para calcular o custo real e o valor da hora trabalhada."""

def calculate_real_cost(cost_data):
    """Calcula o custo real e o valor da hora trabalhada com base nas despesas fornecidas.

    Args:
        cost_data (dict): Dicionário com os custos mensais e horas trabalhadas.

    Returns:
        dict: Cálculo do custo real total e o valor da hora trabalhada.
    """
    # Custos mensais
    custos_fixos = cost_data.get('custos_fixos', {})
    horas_trabalhadas = cost_data.get('horas_trabalhadas', 160)  # Default: 160 horas/mês

    # Somar os custos fixos mensais
    total_custos = sum(custos_fixos.values())

    # Calcular o valor da hora trabalhada
    valor_hora = total_custos / horas_trabalhadas

    return {
        'total_custos': total_custos,
        'valor_hora': valor_hora
    }
