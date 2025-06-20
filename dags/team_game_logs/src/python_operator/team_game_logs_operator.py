from common.NBAHandler import NBAHandler
from common.PostgresHandler import PostgresHandler
from team_game_logs.conf.variables import DB_SCHEMA, TEAM_GAME_LOGS_TABLE
import pandas as pd

def extract_team_game_logs(**context):
    handler = PostgresHandler()
    nba_handler = NBAHandler()
    handler.create_table(
        table_name=TEAM_GAME_LOGS_TABLE['name'],
        columns=TEAM_GAME_LOGS_TABLE['columns'],
        schema=DB_SCHEMA
    )
    seasons = [f"{y}-{str(y+1)[2:]}" for y in range(2016, 2025)]
    season_types = ['Regular Season', 'Playoffs']
    all_data = []
    for season in seasons:
        for season_type in season_types:
            df = nba_handler.get_team_game_logs(season, season_type)
            all_data.append(df)
    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        handler.insert_data(
            df=result,
            table_name=TEAM_GAME_LOGS_TABLE['name'],
            schema=DB_SCHEMA,
            if_exists='replace'
        )
    handler.close_connection() 