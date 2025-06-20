from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from draft_history.src.python_operator.draft_history_operator import extract_draft_history

with DAG(
    'nba_draft_history',
    default_args={'owner': 'airflow', 'retries': 1},
    description='Extract NBA draft history for each season since 2012',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['nba', 'draft'],
) as dag:
    start = EmptyOperator(task_id='start')
    extract_task = PythonOperator(
        task_id='extract_draft_history',
        python_callable=extract_draft_history,
    )
    end = EmptyOperator(task_id='end')

    start >> extract_task >> end 