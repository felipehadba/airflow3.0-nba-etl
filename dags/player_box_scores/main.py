from __future__ import annotations

import pendulum

from airflow.models.dag import DAG

from player_box_scores.src.python_operator.player_box_scores_operator import (
    extract_player_box_scores,
)


with DAG(
    dag_id="player_box_scores",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["nba", "bronze"],
) as dag:
    extract_player_box_scores() 