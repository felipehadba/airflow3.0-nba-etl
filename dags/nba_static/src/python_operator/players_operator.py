from typing import Dict, Any
import pandas as pd
from common.NBAHandler import NBAHandler
from common.PostgresHandler import PostgresHandler
from nba_static.conf.variables import DB_SCHEMA, PLAYERS_TABLE


def extract_players(**context) -> None:
    """
    Extract NBA players data and load it into the database.
    """
    # Initialize database handler
    handler = PostgresHandler()
    nba_handler = NBAHandler()
    
    try:
        # Create table if not exists
        handler.create_table(
            table_name=PLAYERS_TABLE['name'],
            columns=PLAYERS_TABLE['columns'],
            schema=DB_SCHEMA
        )
        
        # Get all players
        df = nba_handler.get_players()
        
        # Insert data
        handler.insert_data(
            df=df,
            table_name=PLAYERS_TABLE['name'],
            schema=DB_SCHEMA,
            if_exists='replace'  # Replace existing data
        )
        
    finally:
        handler.close_connection() 