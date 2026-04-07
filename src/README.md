# Source Code Structure

## Overview
This directory contains the modularized components of the FDA Players Intelligence System.

## Directory Structure

```
src/
├── __init__.py                 # Package initialization
├── config.py                  # Configuration and API settings
├── utils.py                   # Utility functions (logging, data persistence)
├── ingestion/                 # Data ingestion and API integration
│   ├── __init__.py
│   ├── api_client.py         # Wyscout API client
│   └── data_fetcher.py       # Data collection and organization
├── features/                  # Data processing and feature engineering
│   ├── __init__.py
│   └── data_processor.py     # Data cleaning, processing, career analysis
└── models/                    # Analysis and modeling
    ├── __init__.py
    └── analysis.py           # Player/competition analysis, scoring
```

## Module Descriptions

### `config.py`
Contains all configuration settings, endpoint definitions, and loads credentials from environment variables.
- Loads API credentials from `.env` file (WYSCOUT_CLIENT_ID, WYSCOUT_CLIENT_SECRET)
- Defines API endpoints
- Competition and endpoint mappings
- Directory paths for data

### `utils.py`
Utility functions for data persistence and logging.
- `DataManager`: Save/load DataFrames, pickle files, JSON
- `Logger`: Formatted console output

### `ingestion/`
Handles data fetching from external APIs.

**`api_client.py`**
- `WyscoutAPIClient`: Low-level API interactions
  - Make authenticated requests
  - Fetch competitions, teams, players
  - Fetch career data, advanced stats, matches

**`data_fetcher.py`**
- `DataFetcher`: High-level data collection
  - Fetch and organize competitions and teams
  - Collect player squads
  - Retrieve player details and career history
  - Build ID-to-name mappings

### `features/`
Data processing and feature engineering.

**`data_processor.py`**
- `DataProcessor`: Data cleaning and preprocessing
  - Create DataFrames from raw lists
  - Filter by role, team, date range
  - Calculate Age
  - Handle missing data
  - Generate statistics

- `CareerAnalyzer`: Career data analysis
  - Filter by competitions
  - Enrich with human-readable names
  - Calculate career statistics

### `models/`
Analysis and modeling.

**`analysis.py`**
- `PlayerAnalyzer`: Player-level analysis
  - Find similar players
  - Rank players by metric
  - Calculate percentiles

- `CompetitionAnalyzer`: Competition-level analysis
  - Player count by team/role
  - Age statistics

- `PerformanceScorer`: Performance scoring
  - Calculate normalized scores
  - Combine weighted metrics

## Usage Example

```python
from src.ingestion import DataFetcher
from src.features import DataProcessor
from src.models import CompetitionAnalyzer
from src.utils import DataManager, Logger

# Fetch data
fetcher = DataFetcher()
teams = fetcher.fetch_competitions_and_teams()
players = fetcher.fetch_all_players_from_competitions(['Serie A', 'Serie B'])

# Process data
processor = DataProcessor()
df = processor.create_players_dataframe(players)
df = processor.add_age_column(df)

# Analyze
analyzer = CompetitionAnalyzer()
team_stats = analyzer.get_age_statistics_by_team(df)

# Save
manager = DataManager()
manager.save_dataframe(df, 'data/processed/players.csv')
```

## Integration with Notebook

The original `PlayerIntelligenceSystem.ipynb` can import from these modules instead of defining everything inline. This provides:
- Code reusability
- Better maintainability
- Easier testing
- Cleaner notebook cells
- Version control friendly code

Example notebook cell:
```python
from src.ingestion import DataFetcher
from src.features import DataProcessor

fetcher = DataFetcher()
players = fetcher.fetch_all_players_from_competitions(['Serie A'])

processor = DataProcessor()
df = processor.create_players_dataframe(players)
df = processor.add_age_column(df)
```
