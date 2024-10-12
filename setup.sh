#!/bin/bash

# Criar diretórios
mkdir -p app_balance/{static,templates,user,tests} assets

# Criar arquivos
touch app_balance/{__init__.py,app.py,commands.py,compat.py,database.py,extensions.py,settings.py,utils.py}
touch app_balance/requirements.txt
touch app_balance/.env
touch app_balance/README.md
touch app_balance/docker-compose.yml
touch app_balance/Dockerfile

# Criar um arquivo de teste
touch app_balance/tests/test_app.py
