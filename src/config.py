"""
Configuration settings for the FDA Players Intelligence System.

All configuration is loaded from environment variables.
Do NOT hardcode any settings here.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# API CREDENTIALS (REQUIRED)
# ============================================================================
CLIENT_ID = os.getenv("WYSCOUT_CLIENT_ID")
CLIENT_SECRET = os.getenv("WYSCOUT_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError(
        "Missing Wyscout API credentials!\n"
        "Please set environment variables in .env file:\n"
        "  WYSCOUT_CLIENT_ID=your_id\n"
        "  WYSCOUT_CLIENT_SECRET=your_secret"
    )

# ============================================================================
# API CONFIGURATION
# ============================================================================
API_BASE = os.getenv("API_BASE_URL")
API_TIMEOUT = int(os.getenv("API_TIMEOUT"))

# ============================================================================
# COMPETITION IDS
# ============================================================================
KNOWN_COMPETITIONS = {
    'Serie A': int(os.getenv("COMPETITION_SERIE_A")),
    'Serie B': int(os.getenv("COMPETITION_SERIE_B")),
    'Serie C': int(os.getenv("COMPETITION_SERIE_C")),
    'Campionato Primavera 1': int(os.getenv("COMPETITION_PRIMAVERA_1"))
}

# Parse active competition IDs from comma-separated string
_active_ids_str = os.getenv("ACTIVE_COMPETITION_IDS")
_active_ids = [int(id.strip()) for id in _active_ids_str.split(",")]

# Build ACTIVE_COMPETITIONS dict dynamically
ACTIVE_COMPETITIONS = {
    name: comp_id 
    for name, comp_id in KNOWN_COMPETITIONS.items() 
    if comp_id in _active_ids
}

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

# ============================================================================
# DATA DIRECTORIES
# ============================================================================
CACHE_DIR = os.getenv("CACHE_DIR", "data/cache")
RAW_DATA_DIR = os.getenv("RAW_DATA_DIR", "data/raw")
PROCESSED_DATA_DIR = os.getenv("PROCESSED_DATA_DIR", "data/processed")

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Optional settings with defaults
MAX_PLAYERS_PER_PAGE = int(os.getenv("MAX_PLAYERS_PER_PAGE", "100"))
REQUEST_RETRY_ATTEMPTS = int(os.getenv("REQUEST_RETRY_ATTEMPTS", "3"))
REQUEST_RETRY_DELAY = int(os.getenv("REQUEST_RETRY_DELAY", "2"))

# ============================================================================
# DEBUG INFO (only in development)
# ============================================================================
if ENVIRONMENT == "development":
    print(f"[CONFIG] Loaded configuration from environment variables")
    print(f"[CONFIG] Active competitions: {list(ACTIVE_COMPETITIONS.keys())}")
    print(f"[CONFIG] Data directories: {CACHE_DIR}, {RAW_DATA_DIR}, {PROCESSED_DATA_DIR}")

