from __future__ import annotations

from logging import getLogger

from airflow.decorators import task
from common.NBAHandler import NBAHandler
from common.PostgresHandler import PostgresHandler
from player_box_scores.conf.variables import (
    player_box_scores_table_schema,
    schema_name,
)

logger = getLogger(__name__)


@task(task_id="extract_player_box_scores")
def extract_player_box_scores():
    """
    Extracts player box scores for the 2024-25 season and loads them into the data_bronze database.
    """
    conn_id = "data_bronze"
    nba_handler = NBAHandler()
    postgres_handler = PostgresHandler(conn_id=conn_id)
    season = "2024-25"
    season_types = ["Regular Season", "Playoffs"]
    table_name = "player_box_scores"

    postgres_handler.create_table(
        table_name=table_name,
        schema=schema_name,
        columns=player_box_scores_table_schema,
    )

    for season_type in season_types:
        logger.info(f"Extracting player box scores for {season} {season_type}.")
        df = nba_handler.get_player_game_logs(season=season, season_type=season_type)

        if not df.empty:
            logger.info(f"Successfully extracted {len(df)} records.")
            postgres_handler.insert_data(
                df=df,
                table_name=table_name,
                schema=schema_name,
                if_exists="append",
            )
            logger.info("Successfully loaded data into the database.")
        else:
            logger.info("No data to load.") 