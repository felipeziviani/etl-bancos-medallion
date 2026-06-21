from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from etl.bronze import executar_bronze
from etl.silver import executar_silver
from etl.gold import executar_gold

default_args = {
    "owner": "felipe",
    "retries": 2,                
    "retry_delay": 300,         
}

with DAG(
    dag_id="pipeline_bancos",
    description="Pipeline Medallion (Bronze -> Silver -> Gold) dos bancos brasileiros",
    default_args=default_args, 
    schedule="@daily",            
    start_date=datetime(2026, 6, 1),
    catchup=False,             
    tags=["medallion", "bancos", "brasilapi"],
) as dag:

    tarefa_bronze = PythonOperator(
        task_id="extrair_bancos_bronze",
        python_callable=executar_bronze,
    )

    tarefa_silver = PythonOperator(
        task_id="transformar_bancos_silver",
        python_callable=executar_silver,
    )

    tarefa_gold = PythonOperator(
        task_id="carregar_bancos_gold",
        python_callable=executar_gold,
    )

    tarefa_bronze >> tarefa_silver >> tarefa_gold