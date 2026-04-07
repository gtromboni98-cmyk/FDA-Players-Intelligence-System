"""
Features module for data processing and feature engineering.
Organized as logical submodules: core, positions, stats, scoring.

BACKWARD COMPATIBILITY:
All features are re-exported here, so existing code like:
    from src.features import DataProcessor, apply_position_mapping, etc.
will continue to work without modification.
"""

# ============================================================================
# Core data processing
# ============================================================================
from .core import DataProcessor, CareerAnalyzer

# ============================================================================
# Position mapping
# ============================================================================
from .positions import (
    generalize_position,
    generalize_position_from_list,
    apply_position_mapping,
    get_available_positions,
    filter_by_position,
    get_position_distribution
)

# ============================================================================
# Match statistics expansion
# ============================================================================
from .stats import (
    extract_total_stats,
    extract_average_stats,
    expand_match_stats,
    extract_positions_from_nested,
    clean_match_stats_df
)

# ============================================================================
# PCA scoring
# ============================================================================
from .scoring import (
    get_pca_score_names,
    get_score_features,
    calculate_single_pca_score,
    calculate_all_pca_scores,
    aggregate_player_scores,
    get_top_players_by_score,
    score_distribution_summary
)

__all__ = [
    # Data Processing
    'DataProcessor',
    'CareerAnalyzer',
    # Position Mapping
    'generalize_position',
    'generalize_position_from_list',
    'apply_position_mapping',
    'get_available_positions',
    'filter_by_position',
    'get_position_distribution',
    # Match Stats Expansion
    'extract_total_stats',
    'extract_average_stats',
    'expand_match_stats',
    'extract_positions_from_nested',
    'clean_match_stats_df',
    # PCA Scoring
    'get_pca_score_names',
    'get_score_features',
    'calculate_single_pca_score',
    'calculate_all_pca_scores',
    'aggregate_player_scores',
    'get_top_players_by_score',
    'score_distribution_summary'
]
