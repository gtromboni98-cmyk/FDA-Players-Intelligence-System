# 🏗️ Project Architecture Overview

## Modular Structure Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│            PlayerIntelligenceSystem.ipynb                        │
│  (Interactive Analysis - Imports from src modules)              │
└──────────────────┬──────────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        │  from src import   │
        │  - ingestion       │
        │  - features        │
        │  - models          │
        │  - utils           │
        │                     │
        └─────────┬───────────┘
                  │
    ┌─────────────┼──────────────┬──────────────┬─────────────┐
    │             │              │              │             │
    ▼             ▼              ▼              ▼             ▼
┌────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐  ┌────────┐
│ Data   │  │Ingestion │  │Features  │  │ Models   │  │ Utils  │
│        │  │          │  │          │  │          │  │        │
│ src/   │→ │ src/     │→ │ src/     │→ │ src/     │→ │ src/   │
│config  │  │ingestion │  │features  │  │ models   │  │ utils  │
│        │  │          │  │          │  │          │  │        │
└────────┘  └──────────┘  └─────────┘  └──────────┘  └────────┘
     │         │              │              │           │
     │         │              │              │           │
     │    ┌────┴───┐      ┌────┴────┐   ┌────┴────┐      │
     │    │        │      │         │   │         │      │
     │    ▼        ▼      ▼         ▼   ▼         ▼      ▼
     │  API    Data   Data    Career  Player  Competition  Data
     │  Client Fetcher Processor Analyzer Analyzer Analyzer Manager
     │                                                      │
     │                                                   Logger
     │                                                      │
     └─────────────────────────────────────────────────────┘
                          │
              ┌───────────┴────────────┐
              │                        │
              ▼                        ▼
         data/raw/              data/processed/
      (API responses)         (Analysis results)
```

## Data Flow

```
┌────────────────────────────────┐
│   Wyscout API                  │
│  (Competitions, Teams, Players)│
└────────────────┬───────────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │   WyscoutAPIClient     │
    │  (API Interactions)    │
    │  9 methods for fetch   │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │   DataFetcher          │
    │  (High-level API)      │
    │  Auto-deduplication    │
    │  ID → Name mapping     │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │   DataProcessor        │
    │  (Data Cleaning)       │
    │  DataFrame creation    │
    │  Age calculation       │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │   Analyzers            │
    │  - PlayerAnalyzer      │
    │  - Competition         │
    │  - PerformanceScorer   │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │   DataManager          │
    │  (Save/Load Data)      │
    │  Multiple formats      │
    └────────────────────────┘
```

## Module Relationships

```
┌─────────────────────────────────────────────────────┐
│                    src/config.py                    │
│  (Shared constants, API endpoints, credentials)    │
└────────┬──────────────────────────────────┬────────┘
         │                                  │
         ▼                                  ▼
    ┌──────────────┐            ┌────────────────────┐
    │   src/utils  │            │  src/ingestion/    │
    │              │            │                    │
    │ - DataManager├───────────→│ - WyscoutAPIClient │
    │ - Logger     │    used by │ - DataFetcher      │
    └──────────────┘            └────────┬───────────┘
                                        │
                                        ▼
                            ┌─────────────────────┐
                            │ src/features/       │
                            │                     │
                            │ - DataProcessor (5) │
                            │ - CareerAnalyzer(5) │
                            └────────┬────────────┘
                                     │
                                     ▼
                            ┌─────────────────────┐
                            │ src/models/         │
                            │                     │
                            │ - PlayerAnalyzer    │
                            │ - CompetitionAnal   │
                            │ - PerformanceScore  │
                            └─────────────────────┘
```

## Class & Method Summary

```
WyscoutAPIClient (9 methods)
├── fetch_competitions()
├── fetch_teams_by_competition()
├── fetch_players_by_team()
├── fetch_paginated_data()
├── fetch_player_career()
├── fetch_player_details()
├── fetch_season_details()
├── fetch_player_advanced_stats()
└── fetch_player_matches()

DataFetcher (5 methods)
├── fetch_competitions_and_teams()
├── fetch_squad_for_team()
├── fetch_player_details()
├── fetch_player_career()
└── fetch_all_players_from_competitions()

DataProcessor (5 static methods)
├── create_players_dataframe()
├── filter_players_by_role()
├── filter_players_by_team()
├── add_age_column()
└── handle_missing_data()

CareerAnalyzer (5 methods)
├── filter_career_by_competitions()
├── enrich_career_data()
└── calculate_career_statistics()

PlayerAnalyzer (3 static methods)
├── find_similar_players()
├── rank_players()
└── calculate_percentiles()

CompetitionAnalyzer (4 static methods)
├── get_team_player_count()
├── get_players_by_role()
├── get_age_statistics_by_team()
└── get_age_statistics_by_role()

PerformanceScorer (2 static methods)
├── calculate_composite_score()
└── combine_scores()

DataManager (5 methods)
├── save_pickle() / load_pickle()
├── save_dataframe() / load_dataframe()
└── save_json() / load_json()

Logger (4 static methods)
├── print_section()
├── print_success()
├── print_error()
└── print_info()
```

## Usage Patterns

### Pattern 1: Simple Data Collection
```
DataFetcher() → fetch_all_players_from_competitions()
                        ↓
                    list[dict]
                        ↓
                   DataProcessor()
                        ↓
                   pd.DataFrame
```

### Pattern 2: Career Analysis
```
DataFetcher() → fetch_player_career()
                        ↓
                   list[dict]
                        ↓
                   CareerAnalyzer()
                        ↓
                   enriched data
```

### Pattern 3: Competition Analysis
```
DataFetcher() → fetch_all_players()
                        ↓
                   DataProcessor()
                        ↓
                   CompetitionAnalyzer()
                        ↓
                   statistics
```

## File Dependencies

```
notebook imports
└── src/__init__.py
    ├── src/config.py
    ├── src/utils.py (uses config)
    ├── src/ingestion/__init__.py
    │   ├── src/ingestion/api_client.py (uses config)
    │   └── src/ingestion/data_fetcher.py (uses api_client, config)
    ├── src/features/__init__.py
    │   └── src/features/data_processor.py (uses config)
    └── src/models/__init__.py
        └── src/models/analysis.py (uses pandas, numpy)
```

## Data Type Flow

```
Wyscout API (JSON)
        │
        ▼
    requests.Response
        │
        ▼
    dict / list[dict]
        │
        ▼
    DataProcessor
        │
        ▼
   pd.DataFrame
        │
    ┌───┴───┐
    │       │
    ▼       ▼
  Save    Analyze
  │       │
  ├─csv   ├─rank
  ├─json  ├─stats
  ├─pkl   ├─filter
  └─parquet└─group
```

## Error Handling Flow

```
API Request
    │
    ├─→ Connection Error ──→ except → return None → print message
    │
    ├─→ HTTP Error ────────→ except → return None → print message
    │
    ├─→ JSON Error ────────→ except → return None → print message
    │
    └─→ Success ───────────→ return data

DataFrame Operation
    │
    ├─→ Missing Column ────→ except → return empty → print message
    │
    ├─→ Type Error ────────→ except → handle gracefully
    │
    └─→ Success ───────────→ return result
```

---

This modular architecture provides:
- ✅ Clear separation of concerns
- ✅ Reusable components
- ✅ Testable code
- ✅ Easy maintenance
- ✅ Scalable design
- ✅ Type safety
- ✅ Comprehensive logging
- ✅ Error resilience
