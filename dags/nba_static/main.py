from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from nba_static.src.python_operator.teams_operator import extract_teams
from nba_static.src.python_operator.players_operator import extract_players


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'nba_static_data',
    default_args=default_args,
    description='Extract NBA static data (teams and players)',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['nba', 'static'],
) as dag:

    task_begin = EmptyOperator(task_id='task_begin')
    task_end = EmptyOperator(task_id='task_end')

    with TaskGroup('extract_group', tooltip='Group for NBA static extract tasks') as extract_group:
        extract_teams_task = PythonOperator(
            task_id='extract_teams',
            python_callable=extract_teams,
        )

        extract_players_task = PythonOperator(
            task_id='extract_players',
            python_callable=extract_players,
        )

        extract_teams_task >> extract_players_task

    task_begin >> extract_group >> task_end
