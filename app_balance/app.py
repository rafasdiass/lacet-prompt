# -*- coding: utf-8 -*-
"""O módulo principal, contendo a função de criação do aplicativo."""
import logging
import sys
from flask import Flask
from app_balance import commands
from app_balance.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    migrate,
    flask_static_digest,
)
from app_balance.settings import Config


def create_app(config_object=Config):
    """Cria a fábrica de aplicação."""
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)

    # Registrar módulos e configurações
    register_extensions(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)

    return app


def register_extensions(app):
    """Registrar extensões do Flask."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_errorhandlers(app):
    """Registrar manipuladores de erros."""
    def handle_exception(error):
        """Manipular exceções internas."""
        app.logger.error(f"Erro interno: {error}")
        return "Erro Interno", 500

    app.errorhandler(Exception)(handle_exception)
    return None


def register_shellcontext(app):
    """Registrar objetos do contexto de shell."""
    def shell_context():
        return {"db": db}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Registrar comandos Click."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configurar loggers."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    if not app.debug:
        handler.setLevel(logging.WARNING)
    return None
