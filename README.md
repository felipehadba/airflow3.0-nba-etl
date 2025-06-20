# Airflow 3.0 NBA ETL Proof of Concept

This project is a **Proof of Concept (POC)** for orchestrating NBA data extraction pipelines using **Apache Airflow 3.0**. It leverages the open-source [`nba_api`](https://github.com/swar/nba_api) Python client to fetch NBA data and loads it into a PostgreSQL database. The project is fully containerized for easy local development and reproducibility.

## Features

- **Airflow 3.0** orchestration with CeleryExecutor, Redis, and PostgreSQL (via Docker Compose)
- **nba_api** integration for fetching up-to-date NBA teams and players data
- Modular Python operators for data extraction and loading
- Example of best practices for Airflow DAG structure, TaskGroups, and custom PythonOperators
- Easily extensible for additional NBA data endpoints

---

## Project Structure

```
airflow3.0-nba-etl/
├── dags/
│   └── nba_static/
│       ├── main.py                # Main DAG definition
│       ├── src/python_operator/
│       │   ├── teams_operator.py  # Extracts teams data
│       │   └── players_operator.py# Extracts players data
│       └── conf/variables.py      # Table/schema config
│   └── common/
│       └── PostgresHandler.py     # DB utility class
├── config/
│   └── airflow.cfg
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml
└── ...
```

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- (Optional) Python 3.7+ if running outside Docker

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/airflow3.0-nba-etl.git
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


---

## Configuration

- **Database Connection:**  
  Uses Airflow connection ID `DATA_BRONZE` (see `PostgresHandler`). By default, this is set up in `docker-compose.yaml` for local development.

---

## Requirements

- Python: 3.7+
- Airflow: 3.0.0+
- Python packages:  
  - `nba_api`
  - `requests`
  - `numpy`
  - `pandas`
  - `psycopg2-binary`

All dependencies are pre-installed in the Docker image.

---

## Troubleshooting

- Ensure Docker resources (CPU/memory) are sufficient for Airflow and PostgreSQL.
- If you change Python dependencies, rebuild the image:  
  ```bash
  docker-compose build
  ```

---

## References

- [`nba_api` GitHub](https://github.com/swar/nba_api)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)

--- 