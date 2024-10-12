# -*- coding: utf-8 -*-
"""
Serviço para gerar prompts para análise financeira e processamento de recebimentos agendados e investimentos.
"""

from typing import Dict, List
import sqlite3
from datetime import datetime


class PromptService:
    """
    Serviço para gerar prompts detalhados para análise financeira, baseado em recebimentos e despesas.
    Também faz sugestões para pagamentos de acordo com os recebimentos agendados e análise de investimentos.
    """

    def __init__(self, db_path: str = 'recebimentos.db'):
        """
        Inicializa o serviço de prompts, conectando-se ao banco de dados SQLite.

        Args:
            db_path (str): Caminho para o banco de dados SQLite onde os recebimentos estão armazenados.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def gerar_prompt_custo_real(self, custos: Dict, valor_hora: float, categorias_custos: Dict,
                                margem_lucro_desejada: float, receita_projetada: float) -> str:
        """
        Gera um prompt detalhado para análise dos custos reais, valor da hora trabalhada e estimativas financeiras,
        utilizando metodologias atuais como análise de margem de contribuição, fluxo de caixa e payback.

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
        margem_contribuicao = receita_projetada - custos['total_custos']  # Lucro bruto

        prompt += (
            f"\nEstimativa de lucro:\n"
            f"Lucro estimado: R$ {lucro_estimado:.2f}\n"
            f"Margem de lucro real: {margem_lucro_real:.2f}%\n"
            f"Margem de Contribuição: R$ {margem_contribuicao:.2f}\n"
            "\nAnálise Financeira Adicional:\n"
            "1. O lucro estimado é suficiente para alcançar a margem de lucro desejada? Se não, quais ajustes podem ser feitos?\n"
            "2. Com base nos custos e na margem de lucro, qual é o valor mínimo que deve ser cobrado por projeto para manter a sustentabilidade financeira?\n"
            "3. Existe espaço para oferecer descontos em projetos sem comprometer a margem de lucro? Se sim, qual seria o percentual máximo de desconto possível?\n"
            "4. Quais estratégias podem ser aplicadas para aumentar a receita ou reduzir custos, mantendo a qualidade dos serviços?\n"
            "5. O valor da hora trabalhada está competitivo em relação ao mercado? Como pode ser ajustado para garantir uma margem de lucro adequada?\n"
        )

        return prompt

    def analisar_recebimentos_para_pagamento(self, valor_a_pagar: float) -> str:
        """
        Analisa os recebimentos agendados e sugere de qual(s) recebimento(s) retirar um valor necessário.

        Args:
            valor_a_pagar (float): Valor que o usuário precisa pagar.

        Returns:
            str: Sugestão de recebimentos que podem ser usados para o pagamento.
        """
        # Consulta os recebimentos agendados no banco de dados
        self.cursor.execute("SELECT data, valor FROM recebimentos ORDER BY data")
        recebimentos = self.cursor.fetchall()

        sugestao = []
        total_acumulado = 0.0

        for recebimento in recebimentos:
            data_recebimento = recebimento[0]
            valor_recebimento = recebimento[1]
            total_acumulado += valor_recebimento

            sugestao.append(f"Recebimento em {data_recebimento}: R$ {valor_recebimento:.2f}")

            if total_acumulado >= valor_a_pagar:
                break

        if total_acumulado < valor_a_pagar:
            return f"Não há recebimentos suficientes para cobrir o valor de R$ {valor_a_pagar:.2f}."

        sugestao_str = "\n".join(sugestao)
        return f"Para pagar R$ {valor_a_pagar:.2f}, você pode usar os seguintes recebimentos agendados:\n{sugestao_str}"

    def analisar_investimentos(self, investimentos: List[Dict[str, float]]) -> str:
        """
        Analisa os investimentos informados e estima quando eles podem ser realizados,
        utilizando metodologias como Payback e ROI.

        Args:
            investimentos (list): Lista de dicionários contendo 'descricao', 'valor' e 'retorno_estimado'.

        Returns:
            str: Sugestão de quando os investimentos podem ser feitos e análise de retorno.
        """
        # Consulta os recebimentos agendados no banco de dados
        self.cursor.execute("SELECT data, valor FROM recebimentos ORDER BY data")
        recebimentos = self.cursor.fetchall()

        total_acumulado = 0.0
        meses_necessarios = []

        for investimento in investimentos:
            valor_investimento = investimento['valor']
            descricao_investimento = investimento['descricao']
            retorno_estimado = investimento['retorno_estimado']

            # Resetar o total acumulado para cada investimento
            total_acumulado = 0.0
            meses = 0

            for recebimento in recebimentos:
                total_acumulado += recebimento[1]
                meses += 1
                if total_acumulado >= valor_investimento:
                    break

            if total_acumulado >= valor_investimento:
                # Payback: tempo necessário para recuperar o investimento
                payback_period = meses
                roi = (retorno_estimado / valor_investimento) * 100

                meses_necessarios.append(
                    f"Para o investimento em '{descricao_investimento}' de R$ {valor_investimento:.2f}, "
                    f"você precisará de aproximadamente {meses} meses para cobrir esse valor.\n"
                    f"Estimativa de ROI: {roi:.2f}%\n"
                    f"Período de Payback: {payback_period} meses."
                )
            else:
                meses_necessarios.append(
                    f"Não será possível cobrir o investimento em '{descricao_investimento}' de R$ {valor_investimento:.2f} "
                    f"nos próximos meses."
                )

        return "\n".join(meses_necessarios)

    def salvar_recebimentos(self, recebimentos: list):
        """
        Salva os recebimentos no banco de dados SQLite.

        Args:
            recebimentos (list): Lista de dicionários contendo 'data' e 'valor'.
        """
        for recebimento in recebimentos:
            self.cursor.execute(
                "INSERT INTO recebimentos (data, valor) VALUES (?, ?)",
                (recebimento['data'], recebimento['valor'])
            )
        self.conn.commit()

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()
