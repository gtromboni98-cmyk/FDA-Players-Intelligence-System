"""
Competition configuration for Italian football leagues.
Defines known competitions and active competition IDs.
"""

import os

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
