# FDA Players Intelligence System

**Smart analytics pipeline** for profiling Italian football players using Wyscout API data. Refactored from monolithic notebook into modular, reusable components.

## What It Does

Transforms raw player data from Wyscout API into **actionable intelligence**:

1. **Fetch** teams and squads from Wyscout API
2. **Build** player profiles with career history
3. **Collect** detailed match-level performance statistics
4. **Clean** data and engineer 60+ performance features
5. **Cluster** players using PCA & K-Means
6. **Score** players on 13 position-specific metrics

## Key Features

- ✅ **Modular 6-phase pipeline** - Run as one script or explore step-by-step
- ✅ **Interactive notebooks** - 5 Jupyter notebooks for exploration
- ✅ **Reusable modules** - Import `src/` components for custom analysis
- ✅ **Secure configuration** - All credentials in `.env` (no hardcoding)
- ✅ **Multiple output formats** - CSV, Parquet, JSON, Pickle support
- ✅ **Comprehensive scoring** - 13 derived metrics per player position

## Project Structure

```
├── scripts/                           # Modular 6-phase pipeline
│   ├── 01_fetch_data.py              # Phase 1: Fetch teams & squads
│   ├── 02_player_profiling.py        # Phase 2: Build player profiles
│   ├── 03_fetch_advanced_stats.py    # Phase 3: Collect match stats
│   ├── 04_data_cleaning.py           # Phase 4: Clean & engineer features
│   ├── 05_pca_clustering.py          # Phase 5: PCA & K-Means clustering
│   ├── 06_position_scoring.py        # Phase 6: Calculate position scores
│   └── pipeline.py                   # Run all phases in sequence
│
├── notebooks/                         # Interactive step-by-step analysis
│   ├── 01_data_exploration.ipynb     # Explore raw API data
│   ├── 02_player_analysis.ipynb      # Player profiles & careers
│   ├── 03_advanced_stats_analysis.ipynb # Match-level statistics
│   ├── 04_clustering_insights.ipynb  # Visualize clusters
│   └── 05_scoring_comparison.ipynb   # Compare final scores
│
├── src/                               # Reusable modular code
│   ├── config.py                     # Configuration from .env
│   ├── utils.py                      # Data I/O & logging
│   ├── ingestion/                    # API data collection
│   │   ├── api_client.py            # Low-level API calls
│   │   └── data_fetcher.py          # High-level data fetching
│   ├── features/                     # Data processing
│   │   ├── data_processor.py        # Cleaning & feature engineering
│   │   └── career_analyzer.py       # Career data analysis
│   └── models/                       # Analysis & scoring
│       └── analysis.py              # Player/competition analysis
│
├── data/                              # Data directories (auto-created)
│   ├── cache/                        # API response cache
│   ├── raw/                          # Raw API data
│   └── processed/                    # Analysis results
│
├── requirements.txt                   # Python dependencies
├── .env                              # Configuration (in .gitignore)
├── .env.example                      # Configuration template
├── ENV_SETUP.md                      # Environment setup guide
├── QUICKSTART.md                     # Usage guide & examples
└── README.md                         # This file
```

## Core Modules

### `src.ingestion` - Fetch Data
- **`WyscoutAPIClient`** - Low-level API interactions with retries
- **`DataFetcher`** - High-level data collection with automatic mappings

### `src.features` - Process Data
- **`DataProcessor`** - Cleaning, preprocessing, statistics
- **`CareerAnalyzer`** - Career data enrichment and analysis

### `src.models` - Analyze Data
- **`PlayerAnalyzer`** - Ranking, similarity, percentiles
- **`CompetitionAnalyzer`** - Team and role statistics
- **`PerformanceScorer`** - Position-specific scoring

### `src.utils` - Utilities
- **`DataManager`** - Persistence (CSV, Parquet, Excel, JSON, Pickle)
- **`Logger`** - Formatted colored output

## Quick Start

### Installation
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Wyscout API credentials
```

### Run Full Pipeline
```bash
python scripts/pipeline.py
```

### Or Explore Interactively
```bash
jupyter notebook
# Open notebooks/01_data_exploration.ipynb
```

See [QUICKSTART.md](QUICKSTART.md) for detailed usage examples and API reference.

## Data Pipeline

```
Wyscout API
    ↓
[1] Fetch competitions & teams → data/cache/
    ↓
[2] Build player profiles → data/processed/
    ↓
[3] Fetch match statistics → data/processed/match_stats.pkl
    ↓
[4] Clean & engineer features → data/processed/players_stats_clean.csv
    ↓
[5] PCA & K-Means clustering → data/processed/pca_clusters.csv
    ↓
[6] Calculate scoring metrics → data/processed/player_position_scores.csv
```

## Usage Options

### 1. Automated Pipeline (Fastest)
```bash
python scripts/pipeline.py
# Runs all 6 phases automatically
# Results in data/processed/
```

### 2. Step-by-Step (Notebooks)
```bash
jupyter notebook
# Open notebooks/ folder for interactive exploration
# Understand each phase in detail
```

### 3. Custom Analysis (Modules)
```python
from src.ingestion import DataFetcher
from src.features import DataProcessor
from src.models import CompetitionAnalyzer

fetcher = DataFetcher()
players = fetcher.fetch_all_players_from_competitions(['Serie A'])

processor = DataProcessor()
df = processor.create_players_dataframe(players)

analyzer = CompetitionAnalyzer()
print(analyzer.get_team_player_count(df))
```

## Configuration

All settings via `.env` file - no code changes needed:

```env
WYSCOUT_CLIENT_ID=your_id
WYSCOUT_CLIENT_SECRET=your_secret
ACTIVE_COMPETITION_IDS=524,527,520      # Series A, B, C
API_BASE_URL=https://apirest.wyscout.com/v3
```

See [ENV_SETUP.md](ENV_SETUP.md) for complete configuration guide.

## Documentation

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | Get started with examples |
| [ENV_SETUP.md](ENV_SETUP.md) | Configure credentials & settings |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Detailed module documentation |

## Output

Results saved to `data/processed/`:
- `player_position_scores.csv` - 13 position-specific scores per player
- `pca_clusters.csv` - Clustering assignments
- `players_stats_clean.csv` - Engineered features

## Requirements

- Python 3.8+
- Wyscout API credentials
- See `requirements.txt` for dependencies

---

**License**: See [LICENSE](LICENSE)

See LICENSE file for details

## 🔍 API Reference

For detailed API documentation, see `src/README.md` and docstrings in individual modules.

---

**Last Updated**: April 2026
**Version**: 0.1.0