# NBA Static Data DAG

This DAG is designed to extract static NBA data, specifically teams and players, and load it into your data platform using Apache Airflow 3.0.2.

## Overview

- **DAG ID:** `nba_static_data`
- **Description:** Extracts NBA static data (teams and players) using Python operators.
- **Schedule:** Not scheduled (manual trigger by default)
- **Start Date:** 2024-01-01
- **Tags:** `nba`, `static`

## Structure

The DAG uses Airflow's `TaskGroup` to organize the extraction tasks and includes empty operators to clearly mark the beginning and end of the workflow:

```
task_begin --> [extract_group: extract_teams --> extract_players] --> task_end
```

- **extract_teams:** Extracts NBA teams data.
- **extract_players:** Extracts NBA players data (runs after teams).
- **task_begin/task_end:** EmptyOperator tasks to mark the DAG boundaries.

## Task Details

- **extract_teams:**  
  Python callable: `extract_teams`  
  Location: `nba_static/src/python_operator/teams_operator.py`

- **extract_players:**  
  Python callable: `extract_players`  
  Location: `nba_static/src/python_operator/players_operator.py`

## Configuration

- **Default Arguments:**  
  - Owner: `airflow`
  - Retries: 1
  - Retry delay: 5 minutes
  - Email on failure/retry: False

- **Variables/Config:**  
  - Custom variables can be set in `nba_static/conf/variables.py` if needed.

## Requirements

- Airflow 3.0.2 (see project Dockerfile and requirements.txt for dependencies)
- Python dependencies: `requests`, `numpy`, `pandas`, `psycopg2-binary`, `nba_api`

## Usage

1. Ensure your Airflow environment is running and the required connections (e.g., Postgres) are configured.
2. Place this DAG in your Airflow `dags/` directory.
3. Trigger the DAG manually from the Airflow UI or CLI.

## Extending

- To add more static data extraction tasks, implement new Python callables in `nba_static/src/python_operator/` and add them to the `extract_group` in the DAG.
