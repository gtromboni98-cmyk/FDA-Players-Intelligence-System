# System Integration & Continuation Guide

This document explains how all components of the FDA Players Intelligence System work together, and how to extend it.

## System Architecture Overview

```
WYSCOUT API
    ↓
WyscoutAPIClient (Low-level API)
    ↓
DataFetcher (High-level collection)
    ↓
[Raw Data: Players, Teams, Career, Stats]
    ↓
DataProcessor (Cleaning & Features)
    ↓
[Processed Data: Features, Statistics]
    ↓
PerformanceScorer (Position Scoring)
    ↓
[Results: Position Scores per Player]
    ↓
Analysis & Visualization
```

## Data Flow Diagram

### Phase 1: Data Fetching (Script 01, Notebook 01)
```
01_fetch_data.py / 01_data_exploration.ipynb
    ↓
WyscoutAPIClient.fetch_competitions()
WyscoutAPIClient.fetch_teams_by_competition()
    ↓
Output: teams_by_competition.pkl, team_id_to_name.json
```

### Phase 2: Player Profiling (Script 02, Notebook 02)
```
02_player_profiling.py / 02_player_analysis.ipynb
    ↓
DataFetcher.fetch_all_players_from_competitions()
    ↓
For each player:
  - fetch_player_details() → Basic info (name, role, team, birth_date)
  - fetch_player_career() → Career history with competitions
  - CareerAnalyzer.enrich_career_data() → Add readable names
    ↓
Output: players_profiles.pkl (DataFrame with all players)
```

### Phase 3: Advanced Stats (Script 03, Notebook 03)
```
03_fetch_advanced_stats.py / 03_advanced_stats_analysis.ipynb
    ↓
For each player in players_profiles.pkl:
  - WyscoutAPIClient.fetch_player_advanced_stats()
    ↓
Output: match_stats.pkl (Raw stats)
```

### Phase 4: Data Cleaning (Script 04)
```
04_data_cleaning.py
    ↓
DataProcessor.handle_missing_data() → Remove nulls
DataProcessor.create_features() → Engineer features
    ↓
Output: players_stats_clean.pkl (Clean features)
```

### Phase 5: Clustering (Script 05, Notebook 04)
```
05_pca_clustering.py / 04_clustering_insights.ipynb
    ↓
StandardScaler() → Normalize features
PCA(n_components=0.95) → Reduce to 95% variance
KMeans() → Cluster players
    ↓
Output: pca_clusters.csv, pca_clustering_models.pkl
```

### Phase 6: Position Scoring (Script 06, Notebook 05)
```
06_position_scoring.py / 05_scoring_comparison.ipynb
    ↓
For each position (Defender, Midfielder, Forward):
  - Calculate composite scores from PCA components
  - Normalize to 0-100 scale
    ↓
Output: player_position_scores.csv
```

## Core Classes & Methods

### WyscoutAPIClient
**Location**: `src/ingestion/api_client.py`

Core methods for direct API interaction:
```python
client = WyscoutAPIClient()

# Fetch competitions
competitions = client.fetch_competitions(area_id="ITA")

# Fetch teams for competition
teams = client.fetch_teams_by_competition(competition_wy_id=524)

# Fetch squad for team
squad = client.fetch_players_by_team(team_wy_id=63044, page=1)

# Fetch player statistics
stats = client.fetch_player_advanced_stats(player_wy_id=20702, page=1)

# Fetch player career
career = client.fetch_player_career(player_wy_id=20702)

# Fetch player details
details = client.fetch_player_details(player_wy_id=20702)
```

### DataFetcher
**Location**: `src/ingestion/data_fetcher.py`

High-level collection methods:
```python
fetcher = DataFetcher()

# Fetch all teams and competitions
teams_by_comp = fetcher.fetch_competitions_and_teams(exclude_primavera=True)

# Fetch squad for specific team
squad = fetcher.fetch_squad_for_team(team_wy_id=63044)

# Get player details (with team mapping)
details = fetcher.fetch_player_details(player_wy_id=20702)

# Get player career (filtered by competitions)
career = fetcher.fetch_player_career(
    player_wy_id=20702, 
    filter_competitions=['Serie A', 'Serie B']
)

# Fetch all players from competitions
all_players = fetcher.fetch_all_players_from_competitions(
    competitions=['Serie A', 'Serie B', 'Serie C']
)
```

### DataProcessor
**Location**: `src/features/data_processor.py`

Data processing and feature engineering:
```python
processor = DataProcessor()

# Create DataFrame from player list
df = processor.create_players_dataframe(players_list)

# Filter by role/position
df_defenders = processor.filter_players_by_role(df, roles=['Defender'])

# Add age column
df = processor.add_age_column(df)

# Handle missing data
df_clean = processor.handle_missing_data(df, strategy='drop')

# Get player statistics
stats = processor.get_player_statistics(df)
```

### CareerAnalyzer
**Location**: `src/features/data_processor.py`

Career data analysis:
```python
analyzer = CareerAnalyzer()

# Filter career by competitions
filtered_career = analyzer.filter_career_by_competitions(
    career_data,
    competitions=['Serie A', 'Serie B']
)

# Enrich career with readable names
enriched = analyzer.enrich_career_data(career_data)

# Calculate career statistics
stats = analyzer.calculate_career_statistics(career_data)
```

### PerformanceScorer
**Location**: `src/models/analysis.py`

Position-based scoring:
```python
scorer = PerformanceScorer()

# Calculate composite score from series
score = scorer.calculate_composite_score(
    series=df_stats['passes'],
    weight=1.0,
    inverse=False  # Higher is better
)

# Combine multiple scores
combined = scorer.combine_scores({
    'defense': defense_score,
    'passing': passing_score,
    'physical': physical_score
})
```

### DataManager
**Location**: `src/utils.py`

Data persistence:
```python
manager = DataManager()

# Save/load pickle
manager.save_pickle(data, 'data/processed/my_file.pkl')
data = manager.load_pickle('data/processed/my_file.pkl')

# Save/load JSON
manager.save_json(data_dict, 'data/cache/my_data.json')
data_dict = manager.load_json('data/cache/my_data.json')

# Save DataFrame
manager.save_dataframe(df, 'data/exports/results.csv', fmt='csv')
```

## Configuration System

**Location**: `src/config.py`

All configuration comes from `.env` file:
```bash
# API Credentials
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret

# Known competitions
KNOWN_COMPETITIONS_SERIE_A=524
KNOWN_COMPETITIONS_SERIE_B=527

# Data directories
CACHE_DIR=data/cache
RAW_DATA_DIR=data/raw
PROCESSED_DATA_DIR=data/processed

# Application settings
API_TIMEOUT=30
LOG_LEVEL=INFO
```

## Extending the System

### Custom Analysis Script

```python
from src.ingestion import DataFetcher
from src.features import DataProcessor, CareerAnalyzer
from src.utils import DataManager

# Initialize
fetcher = DataFetcher()
processor = DataProcessor()
manager = DataManager()

# Load existing data or fetch new
df_players = manager.load_pickle('data/processed/players_profiles.pkl')

# Custom analysis
df_defenders = processor.filter_players_by_role(df_players, roles=['Defender'])

# Process and save results
results = {
    'total_defenders': len(df_defenders),
    'teams': df_defenders['team_name'].unique().tolist(),
    'average_age': df_defenders['birth_date'].apply(lambda x: 2024 - int(x[:4])).mean()
}

manager.save_json(results, 'data/exports/defender_analysis.json')
```

### Adding New Position Scoring

Modify `src/models/analysis.py` to add custom position logic:

```python
def calculate_defender_score(self, df_stats, player_wyid):
    """Calculate defender-specific score"""
    tactics = df_stats.get('tactics', {})
    
    score = (
        self.calculate_composite_score(df_stats.get('tackles', 0), 1.0) * 0.3 +
        self.calculate_composite_score(df_stats.get('interceptions', 0), 1.0) * 0.3 +
        self.calculate_composite_score(df_stats.get('clearances', 0), 1.0) * 0.4
    )
    
    return score / 100 * 100  # Normalize to 0-100
```

### Integrating New Data Sources

To add non-Wyscout data (market value, social media, etc.):

1. Create new fetcher in `src/ingestion/`:
```python
# src/ingestion/market_value_fetcher.py
class TransfermarktFetcher:
    def fetch_player_value(self, player_name):
        # Implementation
        pass
```

2. Import and use in processing pipeline:
```python
from src.ingestion.market_value_fetcher import TransfermarktFetcher

fetcher_tm = TransfermarktFetcher()
market_values = {}
for player in all_players:
    market_values[player['wyId']] = fetcher_tm.fetch_player_value(player['name'])

# Merge with existing data
df_players['market_value'] = df_players['wyId'].map(market_values)
```

## Common Workflows

### Quick Test: Fetch & Display 10 Players

```python
from src.ingestion import DataFetcher
import pandas as pd

fetcher = DataFetcher()
teams = fetcher.fetch_competitions_and_teams(exclude_primavera=True)

# Get first 10 players from Serie A
sample_players = []
for team in teams['Serie A'][:2]:  # First 2 teams
    squad = fetcher.fetch_squad_for_team(team['wyId'])
    sample_players.extend(squad[:5])  # First 5 players per team

df = pd.DataFrame(sample_players)
print(df[['name', 'wyId']])
```

### Compare Two Players

```python
from src.ingestion import DataFetcher
from pprint import pprint

fetcher = DataFetcher()

# Get player 1
player1_career = fetcher.fetch_player_career(20702)
player1_details = fetcher.fetch_player_details(20702)

# Get player 2
player2_career = fetcher.fetch_player_career(405603)
player2_details = fetcher.fetch_player_details(405603)

print("Player 1:")
pprint(player1_details)
print("\nPlayer 2:")
pprint(player2_details)
```

### Filter Players by Criteria

```python
from src.features import DataProcessor
import pandas as pd

df_players = pd.read_pickle('data/processed/players_profiles.pkl')
processor = DataProcessor()

# Filter by role
df_midfielders = processor.filter_players_by_role(df_players, roles=['Midfielder'])

# Filter by team
df_juventus = processor.filter_players_by_team(df_players, team_names=['Juventus'])

# Add age and filter
df = processor.add_age_column(df_players)
df_young = df[df['age'] < 25]

print(f"Young midfielders: {len(df_young[df_young['role'] == 'Midfielder'])}")
```

## Troubleshooting

### API Errors
- Check `.env` credentials
- Verify API subscription is active
- Check API rate limits
- Use `API_TIMEOUT` to adjust timeout

### Missing Data
- Some players may not have stats in all competitions
- Use `handle_missing_data()` with appropriate strategy
- Check raw data in `data/raw/` before processing

### Performance Issues
- Use `sample()` to test with subset first
- Save intermediate results with `DataManager`
- Run scripts sequentially, not parallel (API limits)

## Next Steps

1. **Run the pipeline**: `python scripts/pipeline.py`
2. **Explore notebooks**: Start with `notebooks/01_data_exploration.ipynb`
3. **Extend modules**: Add custom analysis in `src/`
4. **Integrate data**: Add new data sources following the pattern
5. **Build features**: Create web dashboard or API wrapper for results

## Support

See `QUICKSTART.md` for usage examples and `ENV_SETUP.md` for installation details.
