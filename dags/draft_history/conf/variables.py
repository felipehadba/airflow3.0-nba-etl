# Database configuration for draft_history DAG
DB_SCHEMA = 'nba'

DRAFT_HISTORY_TABLE = {
    'name': 'draft_history',
    'columns': {
        'PERSON_ID': 'INTEGER',
        'PLAYER_NAME': 'VARCHAR(100)',
        'SEASON': 'VARCHAR(10)',
        'ROUND_NUMBER': 'VARCHAR(10)',
        'ROUND_PICK': 'VARCHAR(10)',
        'OVERALL_PICK': 'VARCHAR(10)',
        'DRAFT_TYPE': 'VARCHAR(20)',
        'TEAM_ID': 'INTEGER',
        'TEAM_CITY': 'VARCHAR(50)',
        'TEAM_NAME': 'VARCHAR(50)',
        'TEAM_ABBREVIATION': 'VARCHAR(10)',
        'ORGANIZATION': 'VARCHAR(100)',
        'ORGANIZATION_TYPE': 'VARCHAR(50)',
        'PLAYER_PROFILE_FLAG': 'VARCHAR(5)',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    }
} 