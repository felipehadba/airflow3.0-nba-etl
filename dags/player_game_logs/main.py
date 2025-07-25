from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from player_game_logs.src.python_operator.player_game_logs_operator import extract_player_game_logs

with DAG(
    'nba_player_game_logs',
    default_args={'owner': 'airflow', 'retries': 1},
    description='Extract NBA player game logs for all teams, all seasons, both season types',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['nba', 'player_game_logs'],
) as dag:
    start = EmptyOperator(task_id='start')
    extract_task = PythonOperator(
        task_id='extract_player_game_logs',
        python_callable=extract_player_game_logs,
    )
    end = EmptyOperator(task_id='end')

    start >> extract_task >> end 