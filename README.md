
---

# Lacet Prompt - Finance Balance Application

Este é um aplicativo de balanço financeiro desenvolvido para gerenciar e rastrear dados financeiros, incluindo integração com GPT-4 para análise de dados.

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
pip install -r requirements.txt
```

3. Execute o aplicativo:

```bash
python3 main_app.py    
```

---

## Inicialização do Banco de Dados

Para inicializar o banco de dados, siga os seguintes passos:

1. Crie o banco de dados e as tabelas executando o seguinte script:

```bash
python3 app_balance/database.py
```

---

## Estrutura do Projeto

O projeto utiliza uma estrutura de camadas, que inclui:

- **app_balance/gui_app.py**: Interface gráfica desenvolvida em PyQt5 para interação com os dados e visualização de análises.
- **app_balance/database.py**: Script de configuração e criação de banco de dados utilizando SQLAlchemy.
- **app_balance/prompts.py**: Gerador de prompts e integração com o GPT-4 para análise financeira.
- **app_balance/services/openai_service.py**: Serviço de integração com a API da OpenAI para envio e recepção de prompts.

---

## Funcionalidades Principais

- **Análise Financeira Automatizada**: Envio de dados financeiros diretamente para GPT-4 para gerar relatórios e análises automáticas.
- **Upload de Arquivos**: Suporte para upload de arquivos Excel, PDF e DOCX para processamento e análise de dados.
- **Visualização de Gráficos**: Exibição de gráficos de evolução financeira utilizando Seaborn, Matplotlib, e Plotly.

---

## Rodando Testes e Linter

Para rodar os testes e verificar a integridade do projeto:

```bash
python3 -m unittest discover -s tests
```

Para rodar o linter e verificar erros de estilo de código:

```bash
flake8 app_balance
```

---

## Gerenciamento de Assets

Os arquivos estáticos (imagens, fontes, etc.) estão localizados no diretório `assets`. Certifique-se de que os ativos estejam corretamente referenciados no código.

---

## Contato

Caso precise de ajuda ou tenha alguma dúvida, entre em contato através do e-mail ou redes sociais do autor.

---

