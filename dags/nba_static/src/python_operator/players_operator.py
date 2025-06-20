from typing import Dict, Any
import pandas as pd
from nba_api.stats.static import players
from common.PostgresHandler import PostgresHandler
from nba_static.conf.variables import DB_SCHEMA, PLAYERS_TABLE


def extract_players(**context) -> None:
    """
    Extract NBA players data and load it into the database.
    """
    # Initialize database handler
    handler = PostgresHandler()
    
    try:
        # Create table if not exists
        handler.create_table(
            table_name=PLAYERS_TABLE['name'],
            columns=PLAYERS_TABLE['columns'],
            schema=DB_SCHEMA
        )
        
        # Get all players
        players_list = players.get_players()
        
        # Convert to DataFrame
        df = pd.DataFrame(players_list)
        
        # Insert data
        handler.insert_data(
            df=df,
            table_name=PLAYERS_TABLE['name'],
            schema=DB_SCHEMA,
            if_exists='replace'  # Replace existing data
        )
        
    finally:
        handler.close_connection() 