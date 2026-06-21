# ETL Bancos Brasil - Arquitetura Medallion

Pipeline de dados que extrai a lista de bancos brasileiros da Brasil API,
processa em camadas (Bronze, Silver, Gold) e gera uma tabela final pronta
para consumo de negócio.

## Arquitetura

- **Bronze**: dados brutos da API, sem transformação
- **Silver**: dados limpos, sem duplicados, com tipos padronizados
- **Gold**: dados agregados, prontos para consumo de negócio

## Estrutura do projeto

etl_fipe/
├── dags/              # DAGs do Airflow
├── etl/               # Lógica do ETL (bronze, silver, gold)
├── data/              # Dados gerados pelo pipeline
├── main.py            # Roda o pipeline manualmente, sem Airflow
├── requirements.txt
├── docker-compose.yml
└── Dockerfile

## Como rodar localmente

```bash
pip install -r requirements.txt
python main.py
```

## Fonte de dados

- Endpoint: `https://brasilapi.com.br/api/banks/v1`
- Dados: lista de instituições financeiras brasileiras