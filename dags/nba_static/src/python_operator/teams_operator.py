from typing import Dict, Any
import pandas as pd
from nba_api.stats.static import teams
from common.PostgresHandler import PostgresHandler
from nba_static.conf.variables import DB_SCHEMA, TEAMS_TABLE


def extract_teams(**context) -> None:
    """
    Extract NBA teams data and load it into the database.
    """
    # Initialize database handler
    handler = PostgresHandler()
    
    try:
        # Create table if not exists
        handler.create_table(
            table_name=TEAMS_TABLE['name'],
            columns=TEAMS_TABLE['columns'],
            schema=DB_SCHEMA
        )
        
        # Get all teams
        teams_list = teams.get_teams()
        
        # Convert to DataFrame
        df = pd.DataFrame(teams_list)
        
        # Insert data
        handler.insert_data(
            df=df,
            table_name=TEAMS_TABLE['name'],
            schema=DB_SCHEMA,
            if_exists='replace'  # Replace existing data
        )
        
    finally:
        handler.close_connection() 