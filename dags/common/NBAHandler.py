import time
from nba_api.stats.endpoints import TeamGameLogs, PlayerGameLogs
from nba_api.stats.static import teams, players
import pandas as pd

class NBAHandler:
    def get_teams(self):
        """
        Retrieve all NBA teams as a DataFrame.
        Returns:
            pd.DataFrame: DataFrame containing all NBA teams.
        """
        teams_list = teams.get_teams()
        return pd.DataFrame(teams_list)

    def get_players(self):
        """
        Retrieve all NBA players as a DataFrame.
        Returns:
            pd.DataFrame: DataFrame containing all NBA players.
        """
        players_list = players.get_players()
        return pd.DataFrame(players_list)

    def get_team_game_logs(self, season, season_type):
        """
        Retrieve team game logs for a given NBA season and season type.

        Args:
            season (str): NBA season (e.g., '2024-25').
            season_type (str): 'Regular Season' or 'Playoffs'.

        Returns:
            pd.DataFrame: DataFrame containing team game logs for the specified season and type.
        """
        for _ in range(3):
            try:
                resp = TeamGameLogs(season_nullable=season, season_type_nullable=season_type)
                return resp.get_data_frames()[0]
            except Exception:
                time.sleep(1)
        raise

    def get_player_game_logs(self, season, season_type):
        """
        Retrieve player game logs for a given NBA season and season type.

        Args:
            season (str): NBA season (e.g., '2024-25').
            season_type (str): 'Regular Season' or 'Playoffs'.

        Returns:
            pd.DataFrame: DataFrame containing player game logs for the specified season and type.
        """
        for _ in range(3):
            try:
                resp = PlayerGameLogs(season_nullable=season, season_type_nullable=season_type)
                return resp.get_data_frames()[0]
            except Exception:
                time.sleep(1)
        raise 