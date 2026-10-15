# 🌡️ Pipeline IoT — Monitoramento de Temperatura

## Sobre o projeto

Este projeto implementa um pipeline de dados para processar leituras de temperatura de um conjunto de dados IoT, armazená-las em um banco de dados PostgreSQL e apresentar os resultados em um dashboard interativo.

O objetivo é praticar conceitos de Engenharia de Dados, análise de dados, SQL, containers e visualização.

## Tecnologias utilizadas

- **Python** — processamento dos dados
- **Pandas** — leitura, limpeza e transformação do CSV
- **PostgreSQL** — armazenamento dos dados
- **Docker** — execução do banco de dados em um container
- **SQLAlchemy** — conexão entre Python e PostgreSQL
- **SQL** — criação de views analíticas
- **Streamlit** — construção do dashboard
- **Plotly** — gráficos interativos
- **Git e GitHub** — controle de versão

## Funcionalidades

- Leitura e processamento de dados em CSV
- Conversão de datas e temperaturas
- Remoção de registros com campos essenciais inválidos
- Armazenamento dos dados no PostgreSQL
- Criação de views para análise de temperaturas médias, extremas e diárias
- Dashboard com indicadores, filtros, gráficos e tabela de leituras recentes

## Estrutura do projeto

```text
pipeline-iot/
├── data/              # Arquivo CSV de origem (não incluído no primeiro commit)
├── sql/
│   └── views.sql      # Views analíticas
├── app.py             # Dashboard Streamlit
├── pipeline.py        # Processamento e carga dos dados
├── requirements.txt   # Dependências Python
├── .gitignore
└── README.md
```

## Como executar

1. Instale Python, Docker e Git.
2. Inicie o Docker Desktop e configure o PostgreSQL.
3. Crie e ative um ambiente virtual Python.
4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Disponibilize o arquivo CSV esperado pelo pipeline em `data/IOT-temp.csv`.
6. Configure a conexão do PostgreSQL em `pipeline.py` e `app.py`.
7. Execute o pipeline:

   ```bash
   python pipeline.py
   ```

8. Inicie o dashboard:

   ```bash
   streamlit run app.py
   ```

9. Abra o endereço local informado pelo Streamlit, normalmente `http://localhost:8501`.

## Análises disponíveis

- Quantidade de leituras e temperaturas mínima, média e máxima
- Evolução da temperatura média diária
- Comparação entre ambientes internos e externos
- Consulta das leituras mais recentes
- Views SQL para análises complementares

## Observação

Este projeto tem finalidade educacional. Para publicação e uso em outros ambientes, configure as credenciais do banco de dados por variáveis de ambiente e não publique senhas ou informações sensíveis.