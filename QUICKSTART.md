# Quick Start Guide

Get up and running with the FDA Players Intelligence System in minutes.

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Credentials
```bash
cp .env.example .env
```

Edit `.env` and add your Wyscout API credentials:
```env
WYSCOUT_CLIENT_ID=your_client_id_here
WYSCOUT_CLIENT_SECRET=your_client_secret_here
```

See [ENV_SETUP.md](ENV_SETUP.md) for complete configuration guide.

## Three Ways to Use

### 🚀 Option 1: Run Full Pipeline (Fastest)

Automatically run all 6 phases in sequence:

```bash
python scripts/pipeline.py
```

**Output**: Results in `data/processed/`:
- `player_position_scores.csv` - Player scores and rankings
- `pca_clusters.csv` - Cluster assignments
- `players_stats_clean.csv` - Processed player data

**Time**: ~5-15 minutes (depending on API rate limits)

---

### 🔬 Option 2: Explore Step-by-Step with Notebooks

For interactive exploration with detailed explanations:

```bash
jupyter notebook
```

Then open notebooks in this order:

1. **`01_data_exploration.ipynb`** - Understand raw API data
   - View competitions, teams, player structure
   - Fetch sample data

2. **`02_player_analysis.ipynb`** - Analyze player profiles
   - Build DataFrames with demographic data
   - Explore career histories

3. **`03_advanced_stats_analysis.ipynb`** - Study match statistics
   - Analyze performance metrics
   - Engineer features

4. **`04_clustering_insights.ipynb`** - Visualize clusters
   - View PCA results
   - Analyze player groupings

5. **`05_scoring_comparison.ipynb`** - Compare scores
   - Review final rankings
   - Position-specific metrics

---

### 👨‍💻 Option 3: Use Modules Directly

For custom analysis using Python:

```python
from src.ingestion import DataFetcher
from src.features import DataProcessor
from src.models import CompetitionAnalyzer
from src.utils import DataManager

# 1. Fetch data
fetcher = DataFetcher()
players = fetcher.fetch_all_players_from_competitions(['Serie A'])
print(f"Fetched {len(players)} players")

# 2. Process into DataFrame
processor = DataProcessor()
df = processor.create_players_dataframe(players)
df = processor.add_age_column(df)
print(df.head())

# 3. Analyze
analyzer = CompetitionAnalyzer()
team_counts = analyzer.get_team_player_count(df)
print(team_counts)

# 4. Save results
manager = DataManager()
manager.save_dataframe(df, 'data/processed/my_analysis.csv')
```

---

## Common Tasks

### Fetch Serie A Players

```python
from src.ingestion import DataFetcher

fetcher = DataFetcher()
players = fetcher.fetch_all_players_from_competitions(['Serie A'])

# Show basic info
for player in players[:5]:
    print(f"{player['name']} - {player['team_name']} ({player['role']})")
```

### Create Player DataFrame

```python
from src.ingestion import DataFetcher
from src.features import DataProcessor

fetcher = DataFetcher()
players = fetcher.fetch_all_players_from_competitions(['Serie A', 'Serie B'])

processor = DataProcessor()
df = processor.create_players_dataframe(players)
df = processor.add_age_column(df)

print(f"Total players: {len(df)}")
print(f"Average age: {df['age'].mean():.1f} years")
print(f"Teams: {df['team_name'].nunique()}")
```

### Get Team Statistics

```python
from src.models import CompetitionAnalyzer

analyzer = CompetitionAnalyzer()

# Players by team
print("Players per team:")
print(analyzer.get_team_player_count(df))

# Players by role
print("\nPlayers by role:")
print(analyzer.get_players_by_role(df))

# Age statistics by team
print("\nAge statistics by team:")
print(analyzer.get_age_statistics_by_team(df))
```

### Save Data in Multiple Formats

```python
from src.utils import DataManager

manager = DataManager()

# CSV
manager.save_dataframe(df, 'data/processed/players.csv')

# Parquet (compressed)
manager.save_dataframe(df, 'data/processed/players.parquet', fmt='parquet')

# Excel
manager.save_dataframe(df, 'data/processed/players.xlsx', fmt='excel')

# JSON
manager.save_json(df.to_dict(), 'data/processed/players.json')

# Load back
df_loaded = manager.load_dataframe('data/processed/players.csv')
```

### Rank and Compare Players

```python
from src.models import PlayerAnalyzer

analyzer = PlayerAnalyzer()

# Youngest 10 players
youngest = analyzer.rank_players(df, metric='age', ascending=True, top_n=10)
print("Youngest Players:")
print(youngest[['name', 'age', 'team_name']])

# Find similar players
target = {'name': 'Target Player', 'age': 25, 'role': 'Attacker'}
similar = analyzer.find_similar_players(df, target, n_similar=5)
print(f"\nPlayers similar to {target['name']}:")
for player in similar:
    print(f"  {player['name']} - {player['role']} (Age: {player['age']})")
```

### Filter Players by Role

```python
from src.features import DataProcessor

processor = DataProcessor()

# Get attackers only
attackers = processor.filter_players_by_role(df, roles=['Attacker'])
print(f"Attackers: {len(attackers)}")

# Get defenders
defenders = processor.filter_players_by_role(df, roles=['Defender', 'FullBack'])
print(f"Defenders: {len(defenders)}")
```

---

## Core Modules Reference

### `src.ingestion` - Data Collection
- `DataFetcher.fetch_all_players_from_competitions(competition_names)` - Get players
- `DataFetcher.fetch_competitions()` - Get competitions
- `DataFetcher.fetch_teams_by_competition(competition_id)` - Get teams

### `src.features` - Data Processing
- `DataProcessor.create_players_dataframe(players)` - Create DataFrame
- `DataProcessor.add_age_column(df)` - Add age calculation
- `DataProcessor.filter_players_by_role(df, roles)` - Filter by position
- `CareerAnalyzer.enrich_career_data(career)` - Enrich career data

### `src.models` - Analysis & Scoring
- `CompetitionAnalyzer.get_team_player_count(df)` - Count players per team
- `CompetitionAnalyzer.get_players_by_role(df)` - Group by role
- `PlayerAnalyzer.rank_players(df, metric, ascending, top_n)` - Rank players
- `PlayerAnalyzer.find_similar_players(df, target, n_similar)` - Find similar

### `src.utils` - Utilities
- `DataManager.save_dataframe(df, path)` - Save to CSV/Parquet/Excel
- `DataManager.load_dataframe(path)` - Load data
- `Logger.print_section(text)` - Print section header
- `Logger.print_success(text)` - Print success message

---

## Logging & Output

Control logging with `Logger`:

```python
from src.utils import Logger

Logger.print_section("My Analysis")          # Section header
Logger.print_success("Operation completed")   # ✓ Success
Logger.print_error("Something failed")        # ✗ Error
Logger.print_info("Processing...")           # ℹ Info
```

---

## Troubleshooting

### "Missing Wyscout API credentials!"
- Verify `.env` exists: `ls -la .env`
- Check credentials: `grep WYSCOUT_ .env`
- Restart Python after editing `.env`
- See [ENV_SETUP.md](ENV_SETUP.md)

### "No such file" when loading data
- Ensure `scripts/pipeline.py` ran first
- Check file path is correct
- Verify it's in `data/processed/` directory

### API Rate Limiting
- The pipeline handles retries automatically
- If still timing out, increase `API_TIMEOUT` in `.env`
- Alternatively, run notebooks to fetch data incrementally

### Import Errors
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check Python interpreter uses correct virtual environment
- Restart Jupyter kernel if using notebooks

---

## Next Steps

1. **Run the pipeline**: `python scripts/pipeline.py`
2. **Explore results**: Check files in `data/processed/`
3. **Use notebooks**: `jupyter notebook` for interactive analysis
4. **Customize**: Check `src/` for available functions
5. **Read docs**: See [README.md](README.md) and [ENV_SETUP.md](ENV_SETUP.md)

---

**Help needed?** See [README.md](README.md) for project overview or [ENV_SETUP.md](ENV_SETUP.md) for configuration details.
