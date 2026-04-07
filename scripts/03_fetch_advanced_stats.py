"""
FASE 3: Advanced Stats Collection
Scarica statistiche dettagliate match-by-match da API Wyscout.
"""

from src.ingestion import DataFetcher
from src.utils import Logger, DataManager
import pandas as pd

Logger.print_section("FASE 3: Fetching Advanced Match Statistics")

manager = DataManager()
fetcher = DataFetcher()

# Load player profiles
df_players = manager.load_pickle('data/processed/players_profiles.pkl')

Logger.print_info(f"Fetching stats for {len(df_players)} players...")

all_match_stats = []

for idx, player in df_players.iterrows():
    player_wy_id = player.get('wyId')
    
    # Fetch advanced stats using API client
    stats = fetcher.api_client.fetch_player_advanced_stats(player_wy_id)
    if stats and 'advancedstats' in stats:
        for stat in stats['advancedstats']:
            stat['player_name'] = player.get('name')
            stat['player_wyId'] = player_wy_id
            all_match_stats.append(stat)
    
    if (idx + 1) % 10 == 0:
        Logger.print_info(f"  Processed {idx + 1}/{len(df_players)} players")

df_stats = pd.DataFrame(all_match_stats)
Logger.print_success(f"Collected {len(df_stats)} match records")

# Save stats to raw data directory (for use in scripts and notebooks)
manager.save_pickle(df_stats, 'data/raw/match_stats.pkl')
manager.save_dataframe(df_stats, 'data/raw/match_stats.csv')

Logger.print_success("Advanced stats saved to data/raw/")
