from typing import Dict
import pandas as pd

class PromptService:
    """
    Serviço para gerar prompts detalhados para análise financeira e processamento de arquivos.
    Este serviço é focado apenas na criação dos prompts a partir dos dados fornecidos.
    """

    def gerar_prompt_analise(self, custos: Dict, valor_hora: float, categorias_custos: Dict, margem_lucro_desejada: float, receita_projetada: float) -> str:
        """
        Gera um prompt detalhado para análise financeira dos custos, valor da hora trabalhada, e estimativas financeiras.
        """
        return (
            f"Análise financeira:\n"
            f"Total de custos: R$ {custos['total_custos']:.2f}\n"
            f"Valor da hora: R$ {valor_hora:.2f}\n"
            f"Receita projetada: R$ {receita_projetada:.2f}\n"
            f"Margem de lucro desejada: {margem_lucro_desejada}%\n"
            f"\nCategorias de custos:\n" + "\n".join([f"{k}: R$ {v}" for k, v in categorias_custos.items()])
        )

    def processar_arquivo(self, file_path: str, file_type: str) -> Dict:
        """
        Processa arquivos (Excel ou CSV) para extrair dados financeiros.

        Args:
            file_path (str): Caminho para o arquivo.
            file_type (str): Tipo do arquivo (e.g., 'xlsx', 'csv').

        Returns:
            dict: Dados financeiros extraídos do arquivo.
        """
        if file_type == 'xlsx':
            df = pd.read_excel(file_path)
        elif file_type == 'csv':
            df = pd.read_csv(file_path)
        else:
            raise ValueError("Tipo de arquivo não suportado")

        if 'Categoria' not in df.columns or 'Valor' not in df.columns:
            raise ValueError("Arquivo deve conter as colunas 'Categoria' e 'Valor'.")

        categorias_custos = df.groupby('Categoria')['Valor'].sum().to_dict()
        total_custos = df['Valor'].sum()
        receita_projetada = total_custos * 1.5  # Exemplo: receita projetada é 50% maior que os custos

        return {
            'categorias_custos': categorias_custos,
            'total_custos': total_custos,
            'receita_projetada': receita_projetada
        }
