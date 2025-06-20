# Airflow 3.0 NBA ETL Proof of Concept

This project is a **Proof of Concept (POC)** for orchestrating NBA data extraction pipelines using **Apache Airflow 3.0**. It leverages the open-source [`nba_api`](https://github.com/swar/nba_api) Python client to fetch comprehensive NBA data and loads it into a PostgreSQL database. The project is fully containerized for easy local development and reproducibility.

## Features

- **Airflow 3.0** orchestration with CeleryExecutor, Redis, and PostgreSQL (via Docker Compose)
- **nba_api** integration for fetching comprehensive NBA data including:
  - Static data (teams and players)
  - Draft history (since 2012)
  - Player game logs (all teams, all seasons, both season types)
  - Team game logs (all teams, all seasons, both season types)
- Modular Python operators for data extraction and loading
- Example of best practices for Airflow DAG structure, TaskGroups, and custom PythonOperators
- Easily extensible for additional NBA data endpoints

---

## Project Structure

```
airflow3.0-nba-etl/
├── dags/
│   ├── nba_static/                    # Static NBA data (teams & players)
│   │   ├── main.py                    # Main DAG definition
│   │   ├── src/python_operator/
│   │   │   ├── teams_operator.py      # Extracts teams data
│   │   │   └── players_operator.py    # Extracts players data
│   │   ├── conf/variables.py          # Table/schema config
│   │   └── README.md                  # DAG-specific documentation
│   ├── draft_history/                 # NBA draft history data
│   │   ├── main.py                    # Main DAG definition
│   │   ├── src/python_operator/
│   │   │   └── draft_history_operator.py
│   │   └── conf/variables.py          # Table/schema config
│   ├── player_game_logs/              # Player game logs data
│   │   ├── main.py                    # Main DAG definition
│   │   ├── src/python_operator/
│   │   │   └── player_game_logs_operator.py
│   │   └── conf/variables.py          # Table/schema config
│   ├── team_game_logs/                # Team game logs data
│   │   ├── main.py                    # Main DAG definition
│   │   ├── src/python_operator/
│   │   │   └── team_game_logs_operator.py
│   │   └── conf/variables.py          # Table/schema config
│   └── common/                        # Shared utilities
│       ├── NBAHandler.py              # NBA API utility class
│       └── PostgresHandler.py         # Database utility class
├── config/
│   └── airflow.cfg                    # Airflow configuration
├── init-scripts/
│   └── create-databases.sql           # Database initialization
├── logs/                              # Airflow execution logs
├── plugins/                           # Airflow plugins (if any)
├── requirements.txt                   # Python dependencies
├── Dockerfile                         # Custom Airflow image
├── docker-compose.yaml                # Multi-container setup
└── README.md                          # This file
```

---

## Available DAGs

### 1. `nba_static_data`
- **Purpose**: Extracts static NBA data including teams and players information
- **Schedule**: Manual trigger only
- **Tasks**: 
  - `extract_teams`: Fetches all NBA teams data
  - `extract_players`: Fetches all NBA players data
- **Dependencies**: Teams are extracted before players

### 2. `nba_draft_history`
- **Purpose**: Extracts NBA draft history for each season since 2012
- **Schedule**: Manual trigger only
- **Tasks**: `extract_draft_history`: Fetches comprehensive draft data

### 3. `nba_player_game_logs`
- **Purpose**: Extracts NBA player game logs for all teams, all seasons, both season types
- **Schedule**: Manual trigger only
- **Tasks**: `extract_player_game_logs`: Fetches detailed player performance data

### 4. `nba_team_game_logs`
- **Purpose**: Extracts NBA team game logs for all teams, all seasons, both season types
- **Schedule**: Manual trigger only
- **Tasks**: `extract_team_game_logs`: Fetches detailed team performance data

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- (Optional) Python 3.7+ if running outside Docker

### 1. Clone the Repository

```bash
git clone git@github.com:felipehadba/airflow3.0-nba-etl.git
cd airflow3.0-nba-etl
```

### 2. Build and Start the Airflow Stack

```bash
docker-compose up --build
```

This will:
- Build a custom Airflow 3.0 image with all Python dependencies (see `requirements.txt`)
- Start Airflow webserver, scheduler, worker, triggerer, API server, Redis, and PostgreSQL containers
- Initialize the database and create required schemas/tables on first run

### 3. Access the Airflow UI

- Open [http://localhost:8080](http://localhost:8080)
- Default credentials: `airflow` / `airflow` (see `docker-compose.yaml` for overrides)

### 4. Run the DAGs

1. **Static Data**: Start with `nba_static_data` to populate teams and players
2. **Draft History**: Run `nba_draft_history` to get historical draft data
3. **Game Logs**: Run `nba_player_game_logs` and `nba_team_game_logs` for performance data

---

## Configuration

- **Database Connection:**  
  Uses Airflow connection ID `DATA_BRONZE` (see `PostgresHandler`). By default, this is set up in `docker-compose.yaml` for local development.

- **Database Setup:**
  The `init-scripts/create-databases.sql` file automatically creates the required database schema on first run.

---

## Requirements

- Python: 3.7+
- Airflow: 3.0.0+
- Python packages:  
  - `nba_api>=1.2.1`
  - `requests>=2.31.0`
  - `numpy>=1.24.0`
  - `pandas==2.1.2`
  - `psycopg2-binary>=2.9.9`

All dependencies are pre-installed in the Docker image.

---

## Architecture

The project follows a modular architecture:

- **DAGs**: Each data domain has its own DAG with dedicated operators
- **Operators**: Custom PythonOperators handle the specific data extraction logic
- **Handlers**: Shared utility classes (`NBAHandler`, `PostgresHandler`) provide common functionality
- **Configuration**: Each DAG has its own configuration file for table schemas and variables

---

## Troubleshooting

- Ensure Docker resources (CPU/memory) are sufficient for Airflow and PostgreSQL.
- If you change Python dependencies, rebuild the image:  
  ```bash
  docker-compose build
  ```
- Check the logs directory for detailed execution logs
- Monitor the Airflow UI for task status and error messages

---

## References

- [`nba_api` GitHub](https://github.com/swar/nba_api)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Docker Compose](https://airflow.apache.org/docs/docker-stack/index.html)

--- 