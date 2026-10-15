# 🌡️ Pipeline de Dados com IoT e Docker

Projeto acadêmico da disciplina **Disruptive Architectures: IoT, Big Data e IA**, desenvolvido para processar leituras de temperatura de dispositivos IoT, armazenar os dados em PostgreSQL e apresentar análises em um dashboard interativo.

## 🎯 Objetivo

Construir um pipeline de dados que realiza as seguintes etapas:

1. Leitura de um arquivo CSV com dados de temperatura.
2. Tratamento e limpeza dos dados utilizando Python e Pandas.
3. Armazenamento dos registros em um banco PostgreSQL executado com Docker.
4. Criação de views SQL para análises.
5. Visualização dos resultados por meio de um dashboard Streamlit com gráficos Plotly.

## 🛠️ Tecnologias utilizadas

- **Python:** processamento dos dados.
- **Pandas:** leitura, limpeza e transformação do CSV.
- **SQLAlchemy e psycopg2:** conexão entre Python e PostgreSQL.
- **PostgreSQL 16:** armazenamento e consulta dos dados.
- **Docker:** execução do banco de dados em contêiner.
- **Streamlit:** construção do dashboard.
- **Plotly:** criação dos gráficos interativos.
- **Git e GitHub:** versionamento e disponibilização do projeto.

## 📁 Estrutura do projeto

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

## 📊 Dashboard

O dashboard apresenta indicadores gerais, filtros por tipo de ambiente, gráficos de temperatura e uma tabela com as últimas leituras registradas.

### Indicadores principais

- **Total de leituras:** 97.605
- **Temperatura média:** 35,05 °C
- **Temperatura mínima:** 21 °C
- **Temperatura máxima:** 51 °C

### Capturas de tela

As imagens do dashboard serão disponibilizadas na pasta `docs/images/` do repositório.

**Visão geral:**

![Dashboard — indicadores e temperatura ao longo do tempo](docs/images/dashboard-principal.png)

**Gráficos e leituras:**

![Dashboard — gráficos e últimas leituras](docs/images/dashboard-graficos.png)

## 🗄️ Views SQL

As três views estão definidas no arquivo `sql/views.sql`.

### 1. `vw_temperatura_media`

Agrupa os registros por `room_id` e calcula:

- Temperatura média.
- Temperatura mínima.
- Temperatura máxima.
- Quantidade total de leituras.

**Propósito:** resumir os dados por cômodo ou identificador presente na base.

### 2. `vw_temperaturas_extremas`

Retorna as leituras que apresentam a menor ou a maior temperatura registrada.

**Propósito:** facilitar a identificação de valores extremos para investigação e análise. Quando existem registros empatados, a consulta pode retornar mais de duas linhas.

### 3. `vw_resumo_diario`

Agrupa os registros por dia e calcula a média, a mínima, a máxima e a quantidade de leituras.

**Propósito:** analisar a variação da temperatura ao longo do tempo.

## 🔍 Principais resultados e insights

- O banco recebeu **97.605 registros válidos após o tratamento e a remoção de duplicidades**.
- A temperatura média observada foi de **35,05 °C**.
- A menor temperatura encontrada foi de **21 °C**, e a maior foi de **51 °C**.
- A classificação `In` e `Out` permite explorar e comparar leituras de ambientes internos e externos.
- O resumo diário facilita a observação de variações e possíveis valores atípicos.

Esses resultados são referentes ao arquivo histórico utilizado. A interpretação dos extremos deve considerar o contexto de coleta, a unidade de medida e a qualidade dos sensores.

## ⚙️ Como executar o projeto

### 1. Pré-requisitos

Instale:

- Python
- Git
- Docker Desktop

Inicie o Docker Desktop antes de executar os comandos.

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

A senha `sua_senha` é apenas um exemplo para ambiente local. Se escolher outra senha, utilize-a também na configuração da conexão.

Se o contêiner já existir e estiver parado, utilize:

```powershell
docker start postgres-iot
```

### 6. Configurar a conexão com o banco

Crie um arquivo chamado `.env` na pasta principal do projeto:

```env
DATABASE_URL=postgresql+psycopg2://iot_user:sua_senha@localhost:5432/iot_db
```

A senha deve corresponder à configurada na criação do contêiner.

**Importante:** não publique o arquivo `.env`. Ele está incluído no `.gitignore` para manter as configurações locais fora do GitHub.

### 7. Executar o pipeline de dados

Com o banco em execução e o ambiente virtual ativado:

```powershell
python pipeline.py
```

O script lê `data/IOT-temp.csv`, ajusta os tipos de dados, remove registros inválidos e duplicados e insere os dados no PostgreSQL.

**Atenção:** o script recria a tabela de leituras durante a carga. Execute-o antes de criar ou recriar as views, pois uma nova carga pode remover as views existentes.

### 8. Criar as views SQL

Copie o arquivo SQL para o contêiner:

```powershell
docker cp sql/views.sql postgres-iot:/tmp/views.sql
```

Execute as consultas no banco:

```powershell
docker exec -it postgres-iot psql -U iot_user -d iot_db -f /tmp/views.sql
```

Esse procedimento cria ou atualiza as três views utilizadas nas análises.

### 9. Executar o dashboard

Com o banco em execução, inicie o dashboard:

```powershell
streamlit run app.py
```

Abra no navegador o endereço informado pelo Streamlit, normalmente:

http://localhost:8501

## 🧪 Verificar os dados no PostgreSQL

Para consultar a quantidade de registros:

```powershell
docker exec -it postgres-iot psql -U iot_user -d iot_db -c "SELECT COUNT(*) FROM leituras_temperatura;"
```

Para listar as views disponíveis:

```powershell
docker exec -it postgres-iot psql -U iot_user -d iot_db -c "SELECT table_name FROM information_schema.views WHERE table_schema = 'public' ORDER BY table_name;"
```

## 🌐 Fonte dos dados

Dataset **Temperature Readings: IoT Devices**, disponibilizado no Kaggle:

https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices

O arquivo CSV utilizado está incluído na pasta `data/`.

## 🔧 Comandos Git utilizados

Inicializar um repositório:

```bash
git init
```

Adicionar arquivos ao controle de versão:

```bash
git add .
```

Criar um commit:

```bash
git commit -m "Descrição das alterações"
```

Configurar o repositório remoto:

```bash
git remote add origin https://github.com/Denis-Marques/pipeline-iot.git
```

Enviar as alterações:

```bash
git push
```

Atualizar a cópia local:

```bash
git pull
```

## 👨‍💻 Autor

**Denis Marques**

Repositório: https://github.com/Denis-Marques/pipeline-iot
