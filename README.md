

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
2. Crie um ambiente virtual (opcional, mas recomendado):

   - No macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - No Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. Instale as dependências Python:

```bash
pip install -r requirements.txt
```

4. Execute o aplicativo:

```bash
python3 main_app.py
```

---

## Inicialização do Banco de Dados

Como o banco de dados já está incluído no repositório, não é necessário criá-lo manualmente. Basta seguir as etapas acima para rodar o projeto e o banco será utilizado automaticamente.

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
- **Visualização de Gráficos**: Exibição de gráficos de evolução financeira utilizando Seaborn, Matplotlib e Plotly.

---

## Gerar o `requirements.txt`

Se houver necessidade de gerar um novo arquivo `requirements.txt`, siga os passos:

1. Ative seu ambiente virtual (se estiver usando):
   
   ```bash
   source venv/bin/activate  # Para macOS/Linux
   .\venv\Scripts\activate   # Para Windows
   ```

2. Gere o arquivo `requirements.txt`:
   
   ```bash
   pip freeze > requirements.txt
   ```

---

## Remoção de Bibliotecas Não Utilizadas

Para remover bibliotecas não utilizadas, execute o seguinte comando para cada biblioteca:

```bash
pip uninstall <nome-da-biblioteca>
```


---

## Contato

Caso precise de ajuda ou tenha alguma dúvida, entre em contato através do e-mail ou redes sociais do autor.

---

## Versões Utilizadas

- **Python**: 3.9.6
- **Pip**: 24.2

---



