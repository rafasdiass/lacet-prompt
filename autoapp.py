# -*- coding: utf-8 -*-
"""Create an application instance."""
from app_balance.app import create_app
from app_balance.settings import Config

# Cria a instância da aplicação com as configurações especificadas
app, dash_app = create_app(config_object=Config)
