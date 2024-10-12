# -*- coding: utf-8 -*-
"""O módulo principal, contendo a função de criação do aplicativo."""
import logging
import sys

from flask import Flask, render_template
from dash import Dash, dcc, html  # Importando o dcc e html do Dash
import dash_bootstrap_components as dbc

from app_balance import commands, user
from app_balance.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    login_manager,
    migrate,
    flask_static_digest,
)
from app_balance.settings import Config


def create_app(config_object=Config):
    """Cria a fábrica de aplicação.

    :param config_object: O objeto de configuração a ser usado.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)

    # Configurar o Dash
    dash_app = configure_dash(app)

    # Registrar módulos e configurações
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)

    return app, dash_app


def configure_dash(server):
    """Configura o aplicativo Dash."""
    dash_app = Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/dash/',
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )
    dash_app.layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Análise de Custos"),
                dcc.Graph(id="grafico-exemplo", figure={})  # Exemplo de gráfico
            ])
        ])
    ])

    return dash_app


def register_extensions(app):
    """Registrar extensões do Flask."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Registrar blueprints do Flask."""
    # Certifica-se de que o módulo 'user.routes' está importado corretamente
    from app_balance.user.routes import user_bp
    app.register_blueprint(user_bp)
    return None


def register_errorhandlers(app):
    """Registrar manipuladores de erros."""
    def render_error(error):
        """Renderizar template de erro."""
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Registrar objetos do contexto de shell."""
    def shell_context():
        """Objetos do contexto do shell."""
        return {"db": db, "User": user.models.User}

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
        # Configurações adicionais de log se não estiver no modo de depuração
        handler.setLevel(logging.WARNING)
    return None
