"""
Features module for data processing and feature engineering.
Includes data processing, position mapping, match stats expansion, and PCA scoring.
"""

from .data_processor import DataProcessor, CareerAnalyzer
from .position_mapping import (
    generalize_position,
    generalize_position_from_list,
    apply_position_mapping,
    get_available_positions,
    filter_by_position,
    get_position_distribution
)
from .match_stats_expansion import (
    extract_total_stats,
    extract_average_stats,
    expand_match_stats,
    extract_positions_from_nested,
    clean_match_stats_df
)
from .pca_scoring import (
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
