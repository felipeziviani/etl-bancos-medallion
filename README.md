# ETL Bancos Brasil - Arquitetura Medallion

Pipeline de dados que extrai a lista de bancos brasileiros da [Brasil API](https://brasilapi.com.br/),
processa em camadas (Bronze, Silver, Gold).

Projeto criado com fins de aprendizado de ETL, arquitetura Medallion e orquestração com Airflow.

## Arquitetura

O pipeline segue o padrão **Medallion**, organizando os dados em 3 camadas de qualidade crescente:

| Camada | O que faz | Onde fica |
|---|---|---|
|**Bronze** | Extrai os dados brutos da API, sem nenhuma transformação | `data/bronze/bancos.parquet` |
|**Silver** | Limpa, remove duplicados, padroniza tipos e nomes de colunas | `data/silver/bancos.parquet` |
|**Gold** | Agrega os dados em uma métrica de negócio (bancos por tipo de instituição) | `data/gold/resumo_bancos.parquet` |


## Estrutura do projeto

```
etl_bancos/
├── dags/                       # DAGs do Airflow (orquestração do pipeline)
│   └── pipeline_bancos_dag.py
├── etl/                        # Lógica do ETL em si (sem depender do Airflow)
│   ├── __init__.py
│   ├── bronze.py
│   ├── silver.py
│   └── gold.py
├── data/                       # Dados gerados pelo pipeline (não versionados no Git)
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── main.py                     # Roda o pipeline manualmente, sem Airflow
├── requirements.txt
├── docker-compose.yml          # Sobe o Airflow completo
├── Dockerfile
├── .gitignore
└── README.md
```

## Como rodar localmente (sem Airflow)

```bash
# 1. Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar o pipeline completo
python main.py
```

Cada camada também pode ser rodada isoladamente:

```bash
python -m etl.bronze
python -m etl.silver
python -m etl.gold
```

## Como rodar com Airflow (Docker)

```bash
docker-compose build
docker-compose up airflow-init
docker-compose up -d
```

Depois acesse `http://localhost:8081` (usuário e senha padrão: `airflow` / `airflow`)
e ative a DAG `pipeline_bancos`.

> A porta 8081 (em vez da 8080 padrão) evita conflito caso você já tenha outro
> projeto Airflow rodando na máquina.

## Fonte de dados

- **Endpoint:** `https://brasilapi.com.br/api/banks/v1`
- **Dados:** lista de instituições financeiras brasileiras (nome, código, ISPB)