from __future__ import annotations

import pendulum

from airflow.models.dag import DAG

from team_box_scores.src.python_operator.team_box_scores_operator import (
    extract_team_box_scores,
)


with DAG(
    dag_id="team_box_scores",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["nba", "bronze"],
) as dag:
    extract_team_box_scores() 