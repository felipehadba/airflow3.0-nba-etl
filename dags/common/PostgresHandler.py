import logging
from typing import Optional, Dict

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from airflow.hooks.base import BaseHook

# Set up a logger for this module. Airflow will capture its outputs.
log = logging.getLogger(__name__)


class PostgresHandler:
    """
    A helper class to handle common PostgreSQL operations using SQLAlchemy,
    integrated with Airflow connections.
    """
    def __init__(self, conn_id: str = 'DATA_BRONZE'):
        """
        Initializes the handler with an Airflow connection ID.

        Args:
            conn_id (str): Airflow connection ID. Default: 'DATA_BRONZE'.
        """
        self.conn_id = conn_id
        self.engine: Optional[Engine] = None
        self._connection_string = None
        log.info("PostgresHandler initialized for connection '%s'.", self.conn_id)

    @property
    def connection_string(self) -> str:
        """
        Fetches and returns the SQLAlchemy connection string from the Airflow connection.
        Caches the result to avoid repeated calls.

        Returns:
            str: SQLAlchemy connection string (e.g., 'postgresql+psycopg2://...').
        """
        if not self._connection_string:
            log.info("Fetching connection details for '%s' from Airflow.", self.conn_id)
            conn = BaseHook.get_connection(self.conn_id)
            self._connection_string = conn.get_uri()
        return self._connection_string

    def create_connection(self) -> None:
        """
        Creates the SQLAlchemy engine for database communication.
        The actual connection is established on demand.
        """
        try:
            log.info("Creating SQLAlchemy engine...")
            self.engine = create_engine(self.connection_string)
            log.info("SQLAlchemy engine created successfully.")
        except Exception as e:
            log.error("Failed to create SQLAlchemy engine: %s", e)
            raise

    def create_table(
        self,
        table_name: str,
        columns: Dict[str, str],
        schema: str = 'public',
        if_not_exists: bool = True
    ) -> None:
        """
        Creates a schema (if it does not exist) and a table in the database.

        Args:
            table_name (str): Name of the table to be created.
            columns (Dict[str, str]): Dictionary mapping column names to their SQL types.
            schema (str): Schema name. Default: 'public'.
            if_not_exists (bool): If True, adds 'IF NOT EXISTS' to the query.
        """
        if not self.engine:
            self.create_connection()

        log.info("Starting process to create table '%s.%s'.", schema, table_name)
        try:
            with self.engine.connect() as connection:
                log.info("Ensuring schema '%s' exists.", schema)
                connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))

                column_defs = [f'"{col_name}" {col_type}' for col_name, col_type in columns.items()]
                columns_sql = ", ".join(column_defs)

                if_exists_clause = "IF NOT EXISTS " if if_not_exists else ""
                create_table_sql = f'CREATE TABLE {if_exists_clause}"{schema}"."{table_name}" ({columns_sql})'
                
                log.info("Executing table creation for '%s'.", table_name)
                log.debug("SQL: %s", create_table_sql)
                connection.execute(text(create_table_sql))
                # FIX: Removed connection.commit(). The 'with' block manages the transaction.
            log.info("Table '%s.%s' created or already exists.", schema, table_name)
        except SQLAlchemyError as e:
            log.error("Error creating table '%s.%s': %s", schema, table_name, e)
            raise

    def execute_query(self, query: str, params: Optional[dict] = None) -> pd.DataFrame:
        """
        Executes a read (SELECT) query and returns the results in a DataFrame.

        Args:
            query (str): The SQL query to be executed.
            params (dict, optional): Parameters for the query.

        Returns:
            pd.DataFrame: A DataFrame with the query results.
        """
        if not self.engine:
            self.create_connection()

        log.info("Executing read query...")
        log.debug("Query: %s", query)
        try:
            with self.engine.connect() as connection:
                df = pd.read_sql_query(sql=text(query), con=connection, params=params)
            log.info("Query executed successfully, returned %d row(s).", len(df))
            return df
        except SQLAlchemyError as e:
            log.error("Failed to execute query: %s", e)
            raise

    def insert_data(
        self,
        df: pd.DataFrame,
        table_name: str,
        schema: str = 'public',
        if_exists: str = 'append'
    ) -> None:
        """
        Inserts data from a DataFrame into a PostgreSQL table.
        - 'append': Adds the data to the end of the table.
        - 'replace': Truncates the table and then inserts the new data.

        Args:
            df (pd.DataFrame): DataFrame with the data to be inserted.
            table_name (str): Name of the destination table.
            schema (str): Schema name. Default: 'public'.
            if_exists (str): Behavior if the table already exists ('append' or 'replace').
        """
        if not self.engine:
            self.create_connection()

        if df.empty:
            log.warning("The DataFrame for insertion into table '%s.%s' is empty. No action will be taken.", schema, table_name)
            return

        log.info("Starting insertion of %d row(s) into table '%s.%s' with mode '%s'.", len(df), schema, table_name, if_exists)
        
        try:
            if if_exists == 'replace':
                log.info("'replace' mode selected. Executing TRUNCATE on '%s.%s' before insertion.", schema, table_name)
                with self.engine.connect() as connection:
                    # We use quotes to ensure compatibility with schema/table names with special characters
                    connection.execute(text(f'TRUNCATE TABLE "{schema}"."{table_name}"'))
                log.info("Table '%s.%s' successfully truncated.", schema, table_name)
                # After truncate, the insertion becomes an 'append' into an empty table.
                effective_if_exists = 'append'
            
            elif if_exists == 'append':
                effective_if_exists = 'append'
            
            else:
                raise ValueError(f"Mode '{if_exists}' not supported. Use 'append' or 'replace'.")

            # Data insertion step
            df.to_sql(
                name=table_name,
                con=self.engine,
                schema=schema,
                if_exists=effective_if_exists,
                index=False
            )
            log.info("Data successfully inserted into table '%s.%s'.", schema, table_name)

        except SQLAlchemyError as e:
            log.error("Failed to insert data into table '%s.%s': %s", schema, table_name, e)
            raise
        except Exception as e:
            log.error("An unexpected error occurred during data insertion: %s", e)
            raise

    def close_connection(self) -> None:
        """
        Disposes the engine and all its pooled connections.
        """
        if self.engine:
            log.info("Disposing SQLAlchemy engine connection pool.")
            self.engine.dispose()
            self.engine = None