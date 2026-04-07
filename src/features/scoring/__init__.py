"""
PCA-based scoring module.
Calculates 13 performance dimensions for player evaluation.
"""

from .pca import (
    get_pca_score_names,
    get_score_features,
    calculate_single_pca_score,
    calculate_all_pca_scores,
    aggregate_player_scores,
    get_top_players_by_score,
    score_distribution_summary
)

__all__ = [
    'get_pca_score_names',
    'get_score_features',
    'calculate_single_pca_score',
    'calculate_all_pca_scores',
    'aggregate_player_scores',
    'get_top_players_by_score',
    'score_distribution_summary'
]
