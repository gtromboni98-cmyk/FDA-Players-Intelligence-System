"""
Configuration module for FDA Players Intelligence System.

Loads all configuration from environment variables (.env file).
Provides a centralized, modular configuration interface.

BACKWARD COMPATIBILITY:
All configuration items are re-exported here, so existing code like:
    from src.config import POSITION_MAPPING, PCA_SCORE_DEFINITIONS, etc.
will continue to work without modification.
"""

# ============================================================================
# Import base environment configuration
# ============================================================================
from src.config.base import (
    CLIENT_ID,
    CLIENT_SECRET,
    ENVIRONMENT,
    LOG_LEVEL,
    CACHE_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    API_BASE,
    API_TIMEOUT,
    MAX_PLAYERS_PER_PAGE,
    REQUEST_RETRY_ATTEMPTS,
    REQUEST_RETRY_DELAY,
)

# ============================================================================
# Import competitions
# ============================================================================
from src.config.competitions import (
    KNOWN_COMPETITIONS,
    ACTIVE_COMPETITIONS,
)

# ============================================================================
# Import API endpoints
# ============================================================================
from src.config.endpoints import ENDPOINTS

# ============================================================================
# Import position mapping
# ============================================================================
from src.config.positions import (
    POSITION_MAPPING,
    GENERALIZED_POSITIONS,
)

# ============================================================================
# Import PCA configuration
# ============================================================================
from src.config.pca import (
    PCA_SCORE_DEFINITIONS,
    PCA_N_COMPONENTS,
    MIN_MINUTES_PLAYED,
    MIN_MATCHES_PLAYED,
)

# ============================================================================
# Export everything for backward compatibility
# ============================================================================
__all__ = [
    # Base
    'CLIENT_ID',
    'CLIENT_SECRET',
    'ENVIRONMENT',
    'LOG_LEVEL',
    'CACHE_DIR',
    'RAW_DATA_DIR',
    'PROCESSED_DATA_DIR',
    'API_BASE',
    'API_TIMEOUT',
    'MAX_PLAYERS_PER_PAGE',
    'REQUEST_RETRY_ATTEMPTS',
    'REQUEST_RETRY_DELAY',
    # Competitions
    'KNOWN_COMPETITIONS',
    'ACTIVE_COMPETITIONS',
    # Endpoints
    'ENDPOINTS',
    # Positions
    'POSITION_MAPPING',
    'GENERALIZED_POSITIONS',
    # PCA
    'PCA_SCORE_DEFINITIONS',
    'PCA_N_COMPONENTS',
    'MIN_MINUTES_PLAYED',
    'MIN_MATCHES_PLAYED',
]

# ============================================================================
# Debug info (only in development)
# ============================================================================
if ENVIRONMENT == "development":
    print(f"[CONFIG] Loaded configuration from environment variables")
    print(f"[CONFIG] Active competitions: {list(ACTIVE_COMPETITIONS.keys())}")
    print(f"[CONFIG] Data directories: {CACHE_DIR}, {RAW_DATA_DIR}, {PROCESSED_DATA_DIR}")
    print(f"[CONFIG] Generalized positions: {GENERALIZED_POSITIONS}")
    print(f"[CONFIG] PCA score definitions: {list(PCA_SCORE_DEFINITIONS.keys())}")
    print(f"[CONFIG] PCA filtering: min {MIN_MINUTES_PLAYED} minutes, min {MIN_MATCHES_PLAYED} matches")
