"""
FASE 1: Data Ingestion & Fetching
Estrae team e squad da API Wyscout per competizioni italiane.
"""

from src.ingestion import DataFetcher
from src.utils import Logger, DataManager

Logger.print_section("FASE 1: Fetching Competitions & Teams")

# Fetch competitions and teams
fetcher = DataFetcher()
teams_by_competition = fetcher.fetch_competitions_and_teams(exclude_primavera=False)

Logger.print_success(f"Fetched {len(teams_by_competition)} competitions")

# Save mappings
manager = DataManager()
manager.save_pickle(teams_by_competition, 'data/cache/teams_by_competition.pkl')
manager.save_json(fetcher.team_id_to_name, 'data/cache/team_id_to_name.json')

# Summary
total_teams = sum(len(teams) for teams in teams_by_competition.values())
Logger.print_info(f"Total teams across all competitions: {total_teams}")
Logger.print_info(f"Team ID mappings: {len(fetcher.team_id_to_name)}")

Logger.print_success("Data saved to data/cache/")
