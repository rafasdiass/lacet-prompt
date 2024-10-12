# Testar bibliotecas para garantir que estão instaladas corretamente

def test_flask():
    try:
        from flask import Flask
        app = Flask(__name__)
        print("Flask está instalado e funcionando.")
    except ImportError:
        print("Flask não está instalado corretamente.")

def test_dash():
    try:
        import dash
        print("Dash está instalado e funcionando.")
    except ImportError:
        print("Dash não está instalado corretamente.")

def test_sqlalchemy():
    try:
        from flask_sqlalchemy import SQLAlchemy
        db = SQLAlchemy()
        print("Flask-SQLAlchemy está instalado e funcionando.")
    except ImportError:
        print("Flask-SQLAlchemy não está instalado corretamente.")

def test_pandas():
    try:
        import pandas as pd
        print("Pandas está instalado e funcionando.")
    except ImportError:
        print("Pandas não está instalado corretamente.")

def test_pypdf2():
    try:
        import PyPDF2
        print("PyPDF2 está instalado e funcionando.")
    except ImportError:
        print("PyPDF2 não está instalado corretamente.")

def test_openpyxl():
    try:
        import openpyxl
        print("Openpyxl está instalado e funcionando.")
    except ImportError:
        print("Openpyxl não está instalado corretamente.")

def test_plotly():
    try:
        import plotly
        print("Plotly está instalado e funcionando.")
    except ImportError:
        print("Plotly não está instalado corretamente.")

def test_dash_bootstrap():
    try:
        import dash_bootstrap_components as dbc
        print("Dash Bootstrap Components está instalado e funcionando.")
    except ImportError:
        print("Dash Bootstrap Components não está instalado corretamente.")

if __name__ == "__main__":
    test_flask()
    test_dash()
    test_sqlalchemy()
    test_pandas()
    test_pypdf2()
    test_openpyxl()
    test_plotly()
    test_dash_bootstrap()
