# -*- coding: utf-8 -*-
"""Controlador para lidar com as solicitações de upload de arquivos e geração de prompts."""

from flask import Blueprint, request, jsonify
from app_balance.file_processing import processar_arquivo_excel, processar_arquivo_pdf, converter_dataframe_para_dict
from app_balance.prompts import gerar_prompt_custo_real

gpt_bp = Blueprint('gpt', __name__)

@gpt_bp.route('/upload', methods=['POST'])
def upload_arquivos():
    """Endpoint para upload de arquivos e geração de prompt."""
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo fornecido"}), 400

    file = request.files['file']
    file_type = file.filename.split('.')[-1].lower()

    try:
        if file_type in ['xlsx', 'xls']:
            # Processa o arquivo Excel
            df = processar_arquivo_excel(file.read())
            categorias_custos = converter_dataframe_para_dict(df)
        elif file_type == 'pdf':
            # Processa o arquivo PDF
            texto_pdf = processar_arquivo_pdf(file.read())
            categorias_custos = {"Texto PDF": texto_pdf}
        else:
            return jsonify({"error": "Tipo de arquivo não suportado"}), 400

        # Exemplo de cálculo para os custos e o valor da hora trabalhada
        total_custos = df['Valor'].sum() if 'Valor' in df else 0
        valor_hora = total_custos / 160  # Exemplo: 160 horas de trabalho por mês
        margem_lucro_desejada = 20.0  # Exemplo de margem de lucro desejada
        receita_projetada = total_custos * 1.5  # Exemplo de receita projetada com margem de 50%

        # Gera o prompt com base nos dados fornecidos
        prompt = gerar_prompt_custo_real(
            {"total_custos": total_custos},
            valor_hora,
            categorias_custos,
            margem_lucro_desejada,
            receita_projetada
        )
        return jsonify({"prompt": prompt}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
