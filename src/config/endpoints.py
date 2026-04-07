"""
API endpoints configuration for Wyscout API v3.
Defines all available endpoints with placeholder variables.
"""

from src.config import API_BASE

# ============================================================================
# API ENDPOINTS
# ============================================================================
ENDPOINTS = {
    'competitions': f"{API_BASE}/competitions",
    'competitions_area': f"{API_BASE}/competitions?areaId=ITA",
    'squad_list': f"{API_BASE}/competitions/{{wyId}}/teams",
    'players': f"{API_BASE}/competitions/{{wyId}}/players",
    'player_career': f"{API_BASE}/players/{{wyId}}/career",
    'seasons': f"{API_BASE}/seasons/{{wyId}}",
    'players_by_team': f"{API_BASE}/teams/{{team_wyId}}/squad",
    'player_details': f"{API_BASE}/players/{{wyId}}",
    'player_advanced_stats': f"{API_BASE}/players/{{wyId}}/advancedstats",
    'player_match_stats': f"{API_BASE}/players/{{wyId}}/matches/{{matchWyId}}/advancedstats",
    'player_matches': f"{API_BASE}/players/{{wyId}}/matches",
    'season_matches': f"{API_BASE}/seasons/{{wyId}}/matches"
}
