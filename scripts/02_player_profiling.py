"""
FASE 2: Player Profiling & Career Data
Costruisce profili giocatori con dati anagrafici e storico carriera.
"""

from src.ingestion import DataFetcher
from src.features import DataProcessor, CareerAnalyzer
from src.utils import Logger, DataManager
import pandas as pd

Logger.print_section("FASE 2: Building Player Profiles")

# Load previous data
manager = DataManager()
team_id_to_name = manager.load_json('data/cache/team_id_to_name.json')

# Fetch all players from active competitions
fetcher = DataFetcher()
players = fetcher.fetch_all_players_from_competitions()

Logger.print_success(f"Fetched {len(players)} players from active competitions")

# Create DataFrame
processor = DataProcessor()
df_players = processor.create_players_dataframe(players)
df_players = processor.add_age_column(df_players)

Logger.print_success(f"Created DataFrame with {len(df_players)} players")

# Optional: Enrich with career data (for sample)
career_analyzer = CareerAnalyzer(team_id_to_name)
sample_size = min(20, len(df_players))  # Sample first 20

Logger.print_info(f"Fetching career data for {sample_size} sample players...")
players_with_career = []

for idx, row in df_players.head(sample_size).iterrows():
    player_wy_id = row.get('wyId')
    if player_wy_id:
        career = fetcher.fetch_player_career(player_wy_id)
        if career:
            enriched_career = career_analyzer.enrich_career_data(career)
            row_dict = row.to_dict()
            row_dict['career_entries'] = len(enriched_career)
            players_with_career.append(row_dict)

if players_with_career:
    df_with_career = pd.DataFrame(players_with_career)
    Logger.print_success(f"Enriched {len(df_with_career)} players with career data")

# Save results
manager.save_pickle(df_players, 'data/processed/players_profiles.pkl')
manager.save_dataframe(df_players[['name', 'team_name', 'role', 'age']], 
                       'data/processed/players_summary.csv')

Logger.print_success("Player profiles saved to data/processed/")
