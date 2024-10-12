# -*- coding: utf-8 -*-
"""Configuração do aplicativo.

A maioria das configurações é definida através de variáveis de ambiente.

Para desenvolvimento local, use um arquivo .env para definir
as variáveis de ambiente.
"""
from environs import Env

# Carregar variáveis de ambiente do .env
env = Env()
env.read_env()

class Config:
    """Configurações básicas do aplicativo."""
    ENV = env.str("FLASK_ENV", default="production")
    DEBUG = ENV == "development"
    SECRET_KEY = env.str("SECRET_KEY", default="sua-chave-secreta")

    # Configuração do Banco de Dados
    SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL", default="sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuração do Cache
    CACHE_TYPE = env.str("CACHE_TYPE", default="flask_caching.backends.SimpleCache")
    CACHE_DEFAULT_TIMEOUT = env.int("CACHE_DEFAULT_TIMEOUT", default=300)

    # Configurações de Segurança
    BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)

    # Configurações de Arquivos Estáticos
    SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT", default=0)

    # Configurações de Debug Toolbar
    DEBUG_TB_ENABLED = DEBUG
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Configurações de Log
    LOG_LEVEL = env.str("LOG_LEVEL", default="debug")
