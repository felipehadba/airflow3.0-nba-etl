from common.NBAHandler import NBAHandler
from common.PostgresHandler import PostgresHandler
from nba_static.conf.variables import DB_SCHEMA, TEAMS_TABLE


def extract_teams(**context) -> None:
    """
    Extract NBA teams data and load it into the database.
    """
    handler = PostgresHandler()
    nba_handler = NBAHandler()
    try:
        handler.create_table(
            table_name=TEAMS_TABLE['name'],
            columns=TEAMS_TABLE['columns'],
            schema=DB_SCHEMA
        )
        df = nba_handler.get_teams()
        handler.insert_data(
            df=df,
            table_name=TEAMS_TABLE['name'],
            schema=DB_SCHEMA,
            if_exists='replace'
        )
    finally:
        handler.close_connection() 