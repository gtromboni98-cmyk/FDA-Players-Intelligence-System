# Scripts - Modular Pipeline Phases

Estrai il notebook monolitico in **6 fasi indipendenti**. Ogni script fa **una cosa sola**, bene.

## Run Full Pipeline

```bash
python pipeline.py
```

Eseguire tutte le fasi in sequenza:
1. Fetch data from Wyscout API
2. Build player profiles with career
3. Fetch detailed match statistics  
4. Clean data & engineer features
5. PCA & K-Means clustering
6. Calculate 13 position-specific scores

## Run Individual Phases

Se vuoi correre solo alcune fasi:

```bash
python 01_fetch_data.py
python 02_player_profiling.py
python 03_fetch_advanced_stats.py
python 04_data_cleaning.py
python 05_pca_clustering.py
python 06_position_scoring.py
```

## Output

Ogni script salva risultati in `data/`:
- Phase 1-2: `data/cache/` (team mappings, player profiles)
- Phase 3: `data/processed/match_stats.pkl`
- Phase 4: `data/processed/players_stats_clean.csv`
- Phase 5: `data/processed/pca_clusters.csv`
- Phase 6: `data/processed/player_position_scores.csv`

## Development

Estendi le fasi aggiungendo logica custom:

```python
# Custom script
from src.ingestion import DataFetcher
from src.utils import DataManager

manager = DataManager()
df = manager.load_pickle('data/processed/players_stats_clean.pkl')

# Your analysis...
```

---

**Preferisci jupyter?** → Usa folder `notebooks/` per analisi interattiva
