# Notebooks - Interactive Step-by-Step Analysis

**Explore, visualize, and understand** dati e risultati passo dopo passo.

## Available Notebooks

| Notebook | Purpose |
|----------|---------|
| `01_data_exploration.ipynb` | Explore raw API data - competitions, teams, players |
| `02_player_analysis.ipynb` | Player profiles, career analysis, PCA insights |
| `03_advanced_stats_analysis.ipynb` | Match-level statistics, feature distributions |
| `04_clustering_insights.ipynb` | Visualize K-Means clusters, group profiles |
| `05_scoring_comparison.ipynb` | Compare position-specific scores, rankings |

## Start Here

```bash
jupyter notebook
```

Then open `01_data_exploration.ipynb` to understand:
- How Wyscout API is structured
- Teams and competitions available
- Raw player information

## Workflow

1. **Explore** raw data (notebook 1)
2. **Review** player profiles (notebook 2)
3. **Analyze** statistics & features (notebook 3)
4. **Visualize** clusters (notebook 4)
5. **Compare** final scores (notebook 5)

## Integration with Scripts

Notebooks complement the scripts:
- **Scripts** → Automated batch processing (pipeline.py)
- **Notebooks** → Interactive exploration & visualization

Run `scripts/pipeline.py` first, then use notebooks to explore results.

## Development

Add cells to notebooks for:
- Custom visualizations
- Deep-dive analysis
- Report generation
- Experimentation

Save processed data to `data/` follow-up or share with team.

---

**Preferisci automation?** → Use `scripts/pipeline.py`
