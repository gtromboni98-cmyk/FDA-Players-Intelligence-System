# Notebooks - Interactive Step-by-Step Analysis

**Explore, visualize, and understand** the data and results through interactive Jupyter notebooks.

## Available Notebooks

| Notebook | Purpose | Time | Data Input |
|----------|---------|------|-----------|
| `01_data_exploration.ipynb` | Fetch teams, explore competitions, understand API structure | 5-10 min | Live API |
| `02_player_analysis.ipynb` | Build player profiles, analyze careers, identify Primavera players | 10-15 min | `players_profiles.pkl` |
| `03_advanced_stats_analysis.ipynb` | Load & clean advanced match statistics, explore feature distributions | 5-10 min | `match_stats.pkl` |
| `04_clustering_insights.ipynb` | Perform PCA, visualize variance explained, analyze clusters | 5 min | `players_stats_clean.pkl` |
| `05_scoring_comparison.ipynb` | Compare position scores, rank players, export final results | 5 min | `player_position_scores.csv` |

## Quick Start

### Option 1: Start Fresh (Load from API)
```bash
# Step 1: Start Jupyter
jupyter notebook

# Step 2: Open 01_data_exploration.ipynb
# Uncomment and run: fetcher = DataFetcher(); all_players = fetcher.fetch_all_players_from_competitions()

# Step 3: Continue with 02, 03, 04, 05
```

### Option 2: Use Pre-computed Data (Faster)
```bash
# First, run the full pipeline
python scripts/pipeline.py

# Then explore results in notebooks
jupyter notebook
# Open any notebook and run the cells
```

## Notebook Descriptions

### 01_data_exploration.ipynb
**Learn how to fetch data from Wyscout API**

- Initialize `DataFetcher`
- Fetch competitions and teams
- Explore squad for a single team
- Get player details (name, birth_date, role, team)
- (Optional) Fetch ALL players from Series A/B/C (takes 20-30 minutes)

**Key Classes Used**: `DataFetcher`, `WyscoutAPIClient`

---

### 02_player_analysis.ipynb
**Analyze player careers and identify interesting subsets**

- Load players from previous stage or from pickle
- Identify players with Primavera experience
- Analyze individual player career history
- Study role/position distribution
- Filter players by criteria

**Key Classes Used**: `CareerAnalyzer`, `DataProcessor`

---

### 03_advanced_stats_analysis.ipynb
**Work with match-level performance metrics**

- Load raw match statistics
- Explore data structure (columns, types, missing values)
- Clean data using `DataProcessor`
- Generate statistical summaries
- Identify outliers

**Key Classes Used**: `DataProcessor`, `DataManager`

---

### 04_clustering_insights.ipynb
**Apply dimensionality reduction and clustering**

- Prepare numeric features for PCA
- Standardize data (StandardScaler)
- Apply PCA with 95% variance threshold
- Visualize explained variance
- Analyze principal components

**Key Classes Used**: scikit-learn (PCA, StandardScaler)

---

### 05_scoring_comparison.ipynb
**Calculate and compare final position scores**

- Load position-specific scores
- Examine top performers by position
- Visualize score distributions
- Join with player details (name, team, role)
- Export final results for use by scouts/coaches

**Key Classes Used**: `DataManager`

---

## Workflow & Dependencies

```
01 (Fetch Data)
    ↓
02 (Player Analysis)
    ↓
03 (Stats Analysis)
    ↓
04 (Clustering)
    ↓
05 (Scoring)
    ↓
Export Results
```

Each notebook can run independently if input files exist.

## Integration with Scripts

**Notebooks** = Interactive exploration at each step  
**Scripts** = Automated batch processing for production

```bash
# Use scripts for full automated pipeline
python scripts/pipeline.py  # Generates all intermediate files

# Then use notebooks to understand and visualize results
jupyter notebook
```

## Running Cells

1. Click on a cell
2. Press `Shift + Enter` to execute
3. Wait for output (marked with ✓ or error)
4. Continue to next cell

**Tip**: Some operations (especially data fetching) can be slow. Uncomment large operations or reduce dataset size for testing.

## Customization

Add your own cells to notebooks for:
- Custom analysis & filters
- Additional visualizations
- Performance benchmarking
- Integration with other data
- Report generation

Example:
```python
# Compare two specific players
player1_df = df_players[df_players['name'] == 'Player Name 1']
player2_df = df_players[df_players['name'] == 'Player Name 2']

compare_df = pd.concat([player1_df, player2_df])
print(compare_df)
```

## Troubleshooting

### "Module not found" error
- Make sure you're running from project root directory
- Verify Python path includes project root: `sys.path.insert(0, str(project_root))`

### "File not found" error
- Check `data/` directory exists
- Run previous notebooks first or run `python scripts/pipeline.py`
- Verify path in notebook matches actual file location

### API timeouts or rate limits
- Increase `API_TIMEOUT` in `.env`
- Reduce batch size or add delays between requests
- Check Wyscout API subscription status

## Export Results

To save analysis from notebooks:
```python
# Save as CSV
df_results.to_csv('data/exports/my_analysis.csv', index=False)

# Save as pickle (preserves types)
import pickle
with open('data/exports/my_analysis.pkl', 'wb') as f:
    pickle.dump(df_results, f)

# Using DataManager
manager = DataManager()
manager.save_csv(df_results, 'data/exports/my_analysis.csv')
manager.save_pickle(df_results, 'data/exports/my_analysis.pkl')
```

## See Also

- [QUICKSTART.md](../QUICKSTART.md) - Usage examples
- [INTEGRATION.md](../INTEGRATION.md) - System architecture & how to extend
- [README.md](../README.md) - Main project overview

---

**Preferisci automation?** → Use `scripts/pipeline.py`
