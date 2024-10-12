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
    
    # Configurações de Ambiente
    ENV = env.str("FLASK_ENV", default="production")
    DEBUG = ENV == "development"
    SECRET_KEY = env.str("SECRET_KEY", default="sua-chave-secreta")

    # Configuração para desativar a parte web e usar GUI
    USE_GUI = env.bool("USE_GUI", default=True)

    # Configuração do Banco de Dados
    SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL", default="sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuração do Cache
    CACHE_TYPE = env.str("CACHE_TYPE", default="flask_caching.backends.SimpleCache")
    CACHE_DEFAULT_TIMEOUT = env.int("CACHE_DEFAULT_TIMEOUT", default=300)

    # Configurações de Segurança
    BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)

    # Configurações de Arquivos Estáticos (apenas se a parte web for mantida)
    SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT", default=0)

    # Configurações de Log
    LOG_LEVEL = env.str("LOG_LEVEL", default="info")

    # Configurações para a interface GUI (se estiver usando uma interface gráfica)
    GUI_WIDTH = env.int("GUI_WIDTH", default=800)
    GUI_HEIGHT = env.int("GUI_HEIGHT", default=600)
    GUI_TITLE = env.str("GUI_TITLE", default="App de Análise de Custos")

