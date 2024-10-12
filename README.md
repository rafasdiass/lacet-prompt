

---

# Lacet Prompt - Finance Balance Application

Este é um aplicativo de balanço financeiro desenvolvido para gerenciar e rastrear dados financeiros.

## Clonando o Repositório

Para começar a utilizar o projeto, você pode cloná-lo diretamente do GitHub:

```bash
git clone https://github.com/rafasdiass/lacet-prompt.git
cd lacet-prompt
```

## Autor

- **Autor:** Rafael Dias (rafaeldiasdev)
- **Email:** rafasdiasdev@gmail.com
- **GitHub:** [https://github.com/rafasdiass](https://github.com/rafasdiass)
- **LinkedIn:** [https://www.linkedin.com/in/rdrafaeldias/](https://www.linkedin.com/in/rdrafaeldias/)

---

## Ambiente de Desenvolvimento Local

Siga os passos abaixo para rodar o projeto localmente:

1. Acesse o diretório `app_balance`.
2. Instale as dependências Python:

```bash
pip install -r requirements/dev.txt
```

3. Instale as dependências Node.js:

```bash
npm install
npm run-script build
```

4. Inicie o aplicativo (Webpack e Flask rodarão simultaneamente):

```bash
npm start
```

Visite `http://localhost:5000` no navegador para visualizar a aplicação.

---

## Inicialização do Banco de Dados

Após instalar seu sistema de banco de dados, crie as tabelas e faça a migração inicial:

```bash
flask db init
flask db migrate
flask db upgrade
```

---

## Abertura de Shell

Para abrir um shell interativo no ambiente local, execute:

```bash
flask shell
```

---

## Rodando Testes e Linter

Para rodar todos os testes localmente:

```bash
flask test
```

Para rodar o linter e verificar erros de estilo de código:

```bash
flask lint
```

Para evitar que o linter faça mudanças automáticas, utilize o argumento `--check`.

---

## Rodando Testes Python Específicos

Para rodar testes específicos de processamento de arquivos e dependências:

```bash
# Para os testes de processamento de arquivos
python3 tests/processar_arquivos_teste.py

# Para verificar dependências
python3 tests/test_dependencies.py
```

---

## Migrações

Quando for necessário fazer uma migração de banco de dados, siga estes passos:

```bash
flask db migrate
flask db upgrade
```

Para adicionar as migrações ao controle de versão:

```bash
git add migrations/*
git commit -m "Add migrations"
```

---

## Gerenciamento de Assets

Arquivos estáticos (imagens, fontes, etc.) colocados dentro do diretório `assets` são copiados para `static/build` pelo Webpack. Use sempre `static_url_for` ao incluir conteúdo estático para garantir que o nome do arquivo contenha o hash correto:

```html
<link rel="shortcut icon" href="{{static_url_for('static', filename='build/favicon.ico') }}">
```

Para configurar o cache de arquivos estáticos por um ano, adicione a seguinte linha ao arquivo `.env`:

```bash
SEND_FILE_MAX_AGE_DEFAULT=31556926  # um ano
```

---

