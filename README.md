# Pipeline de Dados com IoT e Docker

Projeto acadêmico de Engenharia de Dados que utiliza Python, Pandas, PostgreSQL, Docker e Streamlit para processar e analisar leituras de temperatura de dispositivos IoT.

## Objetivo

Construir um pipeline de dados capaz de ler um arquivo CSV, tratar os dados, armazená-los em um banco PostgreSQL e disponibilizar análises por meio de consultas SQL e de um dashboard interativo.

## Tecnologias utilizadas

- Python
- Pandas
- PostgreSQL 16
- Docker
- SQLAlchemy
- Streamlit
- Plotly
- Git e GitHub

## Estrutura do projeto

```text
pipeline-iot/
├── data/
│   └── IOT-temp.csv
├── sql/
│   └── views.sql
├── app.py
├── pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Como executar o projeto

### 1. Pré-requisitos

Instale o Python, o Git e o Docker Desktop. Inicie o Docker Desktop antes de continuar.

### 2. Clonar o repositório

```bash
git clone https://github.com/Denis-Marques/pipeline-iot.git
cd pipeline-iot
```

### 3. Criar e ativar o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```powershell
pip install -r requirements.txt
```

### 5. Criar o banco PostgreSQL com Docker

```powershell
docker run --name postgres-iot -e POSTGRES_USER=iot_user -e POSTGRES_PASSWORD=sua_senha -e POSTGRES_DB=iot_db -p 5432:5432 -d postgres:16
```

Se a porta 5432 já estiver ocupada ou o contêiner já existir, verifique a configuração antes de criar outro.

### 6. Configurar a conexão

Na pasta principal do projeto, crie um arquivo chamado `.env` com o seguinte conteúdo:

```env
DATABASE_URL=postgresql+psycopg2://iot_user:sua_senha@localhost:5432/iot_db
```

A senha deve ser a mesma definida na criação do contêiner PostgreSQL.

**Importante:** o arquivo `.env` contém configurações locais e não deve ser enviado ao GitHub.

### 7. Executar o pipeline

```powershell
python pipeline.py
```

O script lê o CSV, trata os dados inválidos, remove registros duplicados e carrega as leituras no PostgreSQL.

### 8. Criar as views SQL

Depois que o pipeline terminar, execute o conteúdo de `sql/views.sql` no banco `iot_db`, utilizando uma ferramenta PostgreSQL, como o pgAdmin ou o SQL Shell (psql).

As views permitem consultar médias de temperatura, temperaturas extremas e resumos diários.

### 9. Abrir o dashboard

Em outro terminal, com o ambiente virtual ativado:

```powershell
streamlit run app.py
```

Abra no navegador o endereço local informado pelo Streamlit, normalmente `http://localhost:8501`.

## Resultados esperados

- Dados de temperatura armazenados no PostgreSQL.
- Tratamento de valores inválidos e remoção de duplicatas.
- Consultas analíticas disponibilizadas por views SQL.
- Dashboard interativo para explorar as leituras de temperatura.

## Fonte dos dados

Dataset **Temperature Readings: IoT Devices**, disponibilizado no Kaggle. O arquivo utilizado está na pasta `data/`.

## Autor

Denis Marques

Repositório: https://github.com/Denis-Marques/pipeline-iot
