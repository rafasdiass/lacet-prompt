# -*- coding: utf-8 -*-
"""Gerenciamento de prompts para análise de custos e estimativas financeiras, com suporte para arquivos."""

import pandas as pd
import pdfplumber
import logging

def gerar_prompt_custo_real(custos, valor_hora, categorias_custos, margem_lucro_desejada, receita_projetada):
    """Gera um prompt detalhado para análise dos custos reais, valor da hora trabalhada e estimativas financeiras.

    Args:
        custos (dict): Dicionário com os custos totais.
        valor_hora (float): Valor calculado da hora trabalhada.
        categorias_custos (dict): Dicionário com custos detalhados por categoria.
        margem_lucro_desejada (float): Margem de lucro desejada em porcentagem.
        receita_projetada (float): Receita estimada para o período em análise.

    Returns:
        str: O prompt gerado.
    """
    prompt = (
        f"Análise financeira detalhada:\n"
        f"Total de custos mensais: R$ {custos['total_custos']:.2f}\n"
        f"Valor estimado da hora trabalhada: R$ {valor_hora:.2f}\n"
        f"Margem de lucro desejada: {margem_lucro_desejada:.2f}%\n"
        f"Receita projetada: R$ {receita_projetada:.2f}\n"
        "\nCategorias de custos:\n"
    )

    for categoria, valor in categorias_custos.items():
        prompt += f"- {categoria}: R$ {valor:.2f}\n"

    lucro_estimado = receita_projetada - custos['total_custos']
    margem_lucro_real = (lucro_estimado / receita_projetada) * 100 if receita_projetada > 0 else 0

    prompt += (
        f"\nEstimativa de lucro:\n"
        f"Lucro estimado: R$ {lucro_estimado:.2f}\n"
        f"Margem de lucro real: {margem_lucro_real:.2f}%\n"
        "\nBaseado nos dados acima, analise os seguintes pontos:\n"
        "1. O lucro estimado é suficiente para alcançar a margem de lucro desejada? Se não, quais ajustes podem ser feitos?\n"
        "2. Com base nos custos e na margem de lucro, qual é o valor mínimo que deve ser cobrado por projeto para manter a sustentabilidade financeira?\n"
        "3. Existe espaço para oferecer descontos em projetos sem comprometer a margem de lucro? Se sim, qual seria o percentual máximo de desconto possível?\n"
        "4. Quais estratégias podem ser aplicadas para aumentar a receita ou reduzir custos, mantendo a qualidade dos serviços?\n"
        "5. O valor da hora trabalhada está competitivo em relação ao mercado? Como pode ser ajustado para garantir uma margem de lucro adequada?\n"
    )

    return prompt
