

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

Aqui está o fluxo completo, unificado e contínuo, baseado em um único prompt, mostrando todas as partes interligadas desde o estímulo inicial até a persistência dos dados e exibição dos resultados:

---

### 1. **GUI (gui_app.py) — Estímulo**
   - **Responsabilidade**: Captura a interação inicial do usuário (entrada de texto ou arquivo).
   - **Exemplo de Prompt**: O usuário digita "Me fale sobre análise financeira avançada" ou envia um arquivo Excel para processamento.
   - **Ação**: O GUI envia o input (prompt ou arquivo) para o `TextProcessingService` para ser processado.

   ```
   GUI (Input: "Me fale sobre análise financeira avançada" ou arquivo Excel) ===> Envia para o processamento no TextProcessingService
   ```

### 2. **TextProcessingService (processamento de texto) — Tálamo**
   - **Responsabilidade**: Processa o input do usuário e decide qual rota seguir com base na análise do conteúdo.
   - **Exemplo de Ação**: O `TextProcessingService` realiza a limpeza do texto, analisa o conteúdo usando TextBlob e Spacy, e determina que o prompt é relacionado a análise financeira avançada.
   - **Saída**: A rota definida é "advanced_financial", indicando que o `AdvancedFinancialAnalysisService` será chamado.

   ```
   TextProcessingService ===> Limpa o texto ===> Analisa o texto (com TextBlob/Spacy) ===> Rota definida: "advanced_financial"
   ```

### 3. **Análise de Dados — Análise Especializada**
   - **Responsabilidade**: Realiza a análise específica com base na rota decidida.
     - Se for um "greeting", o `GreetingService` responde com uma saudação.
     - Se for uma "piada", o `JokeService` responde com uma piada.
     - Se for "financial", o `FinancialAnalysisService` executa uma análise financeira simples.
     - Se for "advanced_financial", o `AdvancedFinancialAnalysisService` realiza uma análise financeira mais profunda.
   - **Exemplo de Ação**: O `AdvancedFinancialAnalysisService` realiza uma análise completa dos custos, receitas, e ROI, e gera um relatório detalhado.
   - **Saída**: Um relatório financeiro detalhado sobre análise financeira avançada.

   ```
   Rota: "advanced_financial" ===> AdvancedFinancialAnalysisService ===> Realiza análise detalhada (custos, ROI, etc.) ===> Gera relatório financeiro
   ```

### 4. **DataPersistenceService (Memória) — Armazenamento no Banco de Dados**
   - **Responsabilidade**: Persistir os dados gerados no banco de dados, incluindo o prompt e o resultado da análise.
   - **Exemplo de Ação**: Após a geração do relatório financeiro, o `DataPersistenceService` recebe tanto o prompt original quanto o relatório gerado pelo `AdvancedFinancialAnalysisService`. Ele então salva esses dados nas tabelas apropriadas no banco de dados (por exemplo, na tabela de `Prompts` e `GPT4Responses`).
   - **Saída**: O prompt e o relatório financeiro são salvos com sucesso no banco de dados.

   ```
   Decisão final ===> DataPersistenceService ===> Salva no banco de dados (prompt: "Me fale sobre análise financeira avançada" + relatório gerado)
   ```

### 5. **Exibição dos Resultados — Feedback ao Usuário**
   - **Responsabilidade**: Exibir o resultado da análise para o usuário de maneira amigável.
   - **Exemplo de Ação**: O GUI recebe o relatório financeiro gerado pelo `AdvancedFinancialAnalysisService` e apresenta o relatório de forma clara ao usuário.
   - **Saída**: O usuário vê o relatório completo com os detalhes da análise financeira.

   ```
   Resultado final ===> Exibe no GUI ===> O usuário vê o relatório financeiro avançado
   ```

---

### **Fluxo Completo (Em uma linha contínua):**

1. **GUI (Estimulo)**: O usuário insere o texto "Me fale sobre análise financeira avançada" ou envia um arquivo Excel. O GUI captura essa interação e envia o input para o `TextProcessingService`.

   ```
   GUI (Input: "Me fale sobre análise financeira avançada") ===> TextProcessingService
   ```

2. **TextProcessingService (Tálamo)**: O texto é limpo e analisado com ferramentas como TextBlob e Spacy. O serviço então decide que o prompt está relacionado a uma análise financeira avançada e direciona para o `AdvancedFinancialAnalysisService`.

   ```
   TextProcessingService ===> Rota definida: "advanced_financial"
   ```

3. **Análise Especializada (Análise Financeira Avançada)**: O `AdvancedFinancialAnalysisService` realiza uma análise financeira detalhada com base nos custos, receitas, e outros parâmetros, e gera um relatório.

   ```
   AdvancedFinancialAnalysisService ===> Gera relatório financeiro detalhado
   ```

4. **DataPersistenceService (Memória)**: Após a análise, o `DataPersistenceService` persiste tanto o prompt original quanto o relatório gerado no banco de dados para garantir que todas as interações e resultados estão armazenados corretamente.

   ```
   DataPersistenceService ===> Salva prompt e relatório no banco de dados
   ```

5. **Exibição dos Resultados**: Finalmente, o GUI exibe o relatório gerado ao usuário, mostrando os resultados da análise de forma clara e amigável.

   ```
   GUI ===> Exibe relatório financeiro ao usuário
   ```

---

### **Resumo:**

- O fluxo começa com o **usuário inserindo um texto ou arquivo** no GUI.
- Esse input passa pelo **TextProcessingService**, que atua como o "tálamo" para decidir a rota correta com base na análise do texto.
- Dependendo da rota decidida, o serviço específico (como análise financeira) é chamado para realizar a **análise especializada**.
- Após a análise, os resultados são **persistidos no banco de dados**.
- Por fim, os resultados são **exibidos ao usuário**.

---

Esse guia agora reflete o fluxo contínuo e modular da aplicação, levando em consideração os componentes-chave como o processamento de texto (tálamo), análise especializada e persistência de dados.



