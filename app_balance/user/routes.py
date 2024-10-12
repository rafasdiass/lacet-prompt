# -*- coding: utf-8 -*-
"""User routes (sem renderização de templates)."""
from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
def profile():
    """Endpoint de perfil do usuário que retorna uma resposta JSON."""
    # Exemplo de dados do usuário que podem ser retornados
    dados_usuario = {
        "nome": "Usuário Exemplo",
        "email": "usuario@example.com",
        "idade": 30
    }
    
    # Retorna os dados do usuário no formato JSON
    return jsonify(dados_usuario)
