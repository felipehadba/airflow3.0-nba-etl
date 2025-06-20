from common.NBAHandler import NBAHandler
from common.PostgresHandler import PostgresHandler
from draft_history.conf.variables import DB_SCHEMA, DRAFT_HISTORY_TABLE
import pandas as pd

def extract_draft_history(**context):
    handler = PostgresHandler()
    nba_handler = NBAHandler()
    handler.create_table(
        table_name=DRAFT_HISTORY_TABLE['name'],
        columns=DRAFT_HISTORY_TABLE['columns'],
        schema=DB_SCHEMA
    )
    seasons = [str(year) for year in range(2002, 2024)]
    all_data = []
    for season in seasons:
        df = nba_handler.get_draft_history(season)
        all_data.append(df)
    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        handler.insert_data(
            df=result,
            table_name=DRAFT_HISTORY_TABLE['name'],
            schema=DB_SCHEMA,
            if_exists='replace'
        )
    handler.close_connection() 