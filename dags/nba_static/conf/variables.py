# Database configuration
DB_SCHEMA = 'nba'

# Table configurations
TEAMS_TABLE = {
    'name': 'teams',
    'columns': {
        'id': 'INTEGER PRIMARY KEY',
        'full_name': 'VARCHAR(100)',
        'abbreviation': 'VARCHAR(10)',
        'nickname': 'VARCHAR(50)',
        'city': 'VARCHAR(50)',
        'state': 'VARCHAR(50)',
        'year_founded': 'INTEGER',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    }
}

PLAYERS_TABLE = {
    'name': 'players',
    'columns': {
        'id': 'INTEGER PRIMARY KEY',
        'full_name': 'VARCHAR(100)',
        'first_name': 'VARCHAR(50)',
        'last_name': 'VARCHAR(50)',
        'is_active': 'BOOLEAN',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    }
}
