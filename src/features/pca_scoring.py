"""
PCA-based scoring system for player performance evaluation.
Calculates 13 performance dimensions per match, per player role.
Uses configuration from src.config for feature definitions.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings

from src.config import PCA_SCORE_DEFINITIONS, MIN_MINUTES_PLAYED

warnings.filterwarnings('ignore')


def get_pca_score_names() -> List[str]:
    """Returns list of all 13 PCA score names."""
    return list(PCA_SCORE_DEFINITIONS.keys())


def get_score_features(score_name: str) -> List[str]:
    """
    Returns the list of features for a specific PCA score.
    
    Args:
        score_name: Name of the PCA score (e.g., 'DEFENSE_SCORE')
        
    Returns:
        List of feature column names for this score
    """
    return PCA_SCORE_DEFINITIONS.get(score_name, [])


def validate_features_exist(df: pd.DataFrame, features: List[str], score_name: str) -> Tuple[bool, List[str]]:
    """
    Validates that required features exist in DataFrame.
    
    Args:
        df: DataFrame to check
        features: Required feature names
        score_name: Name of score being validated
        
    Returns:
        Tuple of (all_exist: bool, missing_features: List[str])
    """
    missing = [f for f in features if f not in df.columns]
    
    if missing:
        print(f"⚠️  Score '{score_name}': Missing {len(missing)} features: {missing}")
    
    return len(missing) == 0, missing


def calculate_single_pca_score(df: pd.DataFrame, features: List[str], score_name: str, 
                               verbose: bool = False) -> pd.Series:
    """
    Calculates a single PCA score using specified features.
    
    Process:
    1. Extract feature columns
    2. Handle missing values (fill with 0)
    3. Apply StandardScaler normalization
    4. Apply PCA(n_components=1)
    5. Return loadings as weights for each feature
    
    Args:
        df: DataFrame with match data
        features: List of feature column names for this score
        score_name: Name of this score (for logging)
        verbose: Print processing details
        
    Returns:
        Series with PCA score (0.0-1.0 normalized)
    """
    
    # Validate features
    features_available = [f for f in features if f in df.columns]
    
    if not features_available:
        if verbose:
            print(f"  ❌ {score_name}: No features available")
        return pd.Series(0.0, index=df.index)
    
    if len(features_available) < len(features):
        missing = len(features) - len(features_available)
        if verbose:
            print(f"  ⚠️  {score_name}: Using {len(features_available)}/{len(features)} features (missing {missing})")
    
    # Extract data
    X = df[features_available].copy()
    X = X.fillna(0)
    
    # Skip if all values are identical
    if (X.std() == 0).all():
        if verbose:
            print(f"  ⚠️  {score_name}: All values are identical, returning 0")
        return pd.Series(0.0, index=df.index)
    
    # Normalize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # PCA
    pca = PCA(n_components=1)
    score = pca.fit_transform(X_scaled).flatten()
    
    # Clip to [0, 1] range (normalize)
    score_min, score_max = score.min(), score.max()
    if score_max > score_min:
        score = (score - score_min) / (score_max - score_min)
    else:
        score = np.zeros_like(score)
    
    if verbose:
        print(f"  ✅ {score_name}: Explained variance: {pca.explained_variance_ratio_[0]:.3f}")
    
    return pd.Series(score, index=df.index)


def calculate_all_pca_scores(df: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
    """
    Calculates all 13 PCA scores for a DataFrame (one score per column).
    
    Args:
        df: DataFrame with match-level data
        verbose: Print processing details
        
    Returns:
        DataFrame with original data + 13 new score columns
    """
    
    scores_df = df.copy()
    
    if verbose:
        print(f"\n📊 Calculating {len(PCA_SCORE_DEFINITIONS)} PCA scores for {len(df)} records...\n")
    
    for score_name, features in PCA_SCORE_DEFINITIONS.items():
        
        if verbose:
            print(f"  Calculating {score_name} ({len(features)} features)...")
        
        # Validate
        all_exist, missing = validate_features_exist(df, features, score_name)
        
        # Calculate
        scores_df[score_name] = calculate_single_pca_score(
            df, features, score_name, verbose=verbose
        )
    
    if verbose:
        print(f"\n✅ All {len(PCA_SCORE_DEFINITIONS)} scores calculated\n")
    
    return scores_df


def aggregate_player_scores(match_scores_df: pd.DataFrame, 
                           player_id_col: str = 'playerId',
                           verbose: bool = False) -> pd.DataFrame:
    """
    Aggregates match-level PCA scores to player-level statistics.
    
    For each player × score:
    - mean: Average score across all matches
    - std: Standard deviation (consistency)
    - min, max: Range
    - matches_counted: Number of matches included
    
    Args:
        match_scores_df: DataFrame with match-level scores
        player_id_col: Name of player ID column
        verbose: Print details
        
    Returns:
        Player-level aggregated statistics
    """
    
    score_names = get_pca_score_names()
    aggregate_cols = [player_id_col] + score_names
    
    # Filter to required columns
    available_cols = [col for col in aggregate_cols if col in match_scores_df.columns]
    df_agg = match_scores_df[available_cols].copy()
    
    # Group by player
    player_groups = df_agg.groupby(player_id_col)
    
    result_rows = []
    
    for player_id, group in player_groups:
        row = {player_id_col: player_id}
        
        for score_name in score_names:
            if score_name in group.columns:
                scores = group[score_name].dropna()
                
                row[f'{score_name}_mean'] = scores.mean()
                row[f'{score_name}_std'] = scores.std() if len(scores) > 1 else 0.0
                row[f'{score_name}_min'] = scores.min()
                row[f'{score_name}_max'] = scores.max()
        
        row['matches_counted'] = len(group)
        result_rows.append(row)
    
    player_scores_df = pd.DataFrame(result_rows)
    
    if verbose:
        print(f"✅ Aggregated {len(player_scores_df)} unique players")
        print(f"   Scores: {', '.join(score_names)}")
    
    return player_scores_df


def get_top_players_by_score(match_scores_df: pd.DataFrame, 
                            score_name: str,
                            player_id_col: str = 'playerId',
                            top_n: int = 10,
                            min_matches: int = 5) -> pd.DataFrame:
    """
    Returns top N players for a specific PCA score.
    
    Args:
        match_scores_df: DataFrame with match-level scores
        score_name: Name of score to rank by
        player_id_col: Name of player ID column
        top_n: Number of top players to return
        min_matches: Minimum matches to include player in ranking
        
    Returns:
        DataFrame with top players and score statistics
    """
    
    if score_name not in match_scores_df.columns:
        raise ValueError(f"Score '{score_name}' not found in DataFrame")
    
    # Aggregate by player
    player_stats = match_scores_df.groupby(player_id_col).agg({
        score_name: ['mean', 'std', 'count']
    }).reset_index()
    
    player_stats.columns = [player_id_col, f'{score_name}_mean', f'{score_name}_std', 'matches']
    
    # Filter by min matches
    player_stats = player_stats[player_stats['matches'] >= min_matches]
    
    # Sort by score
    player_stats = player_stats.sort_values(f'{score_name}_mean', ascending=False).head(top_n)
    
    return player_stats


def score_distribution_summary(match_scores_df: pd.DataFrame, verbose: bool = True) -> Dict:
    """
    Returns summary statistics for all 13 PCA scores.
    
    Args:
        match_scores_df: DataFrame with match-level scores
        verbose: Print summary
        
    Returns:
        Dictionary with statistics per score
    """
    
    score_names = get_pca_score_names()
    summary = {}
    
    for score_name in score_names:
        if score_name in match_scores_df.columns:
            scores = match_scores_df[score_name].dropna()
            
            summary[score_name] = {
                'count': len(scores),
                'mean': scores.mean(),
                'std': scores.std(),
                'min': scores.min(),
                'max': scores.max(),
                'q25': scores.quantile(0.25),
                'q50': scores.quantile(0.50),
                'q75': scores.quantile(0.75),
            }
    
    if verbose:
        print("\n📊 PCA Score Distribution Summary")
        print("=" * 80)
        for score_name, stats in summary.items():
            print(f"\n{score_name}:")
            print(f"  Count:     {stats['count']:6.0f}")
            print(f"  Mean:      {stats['mean']:6.3f}  |  Std: {stats['std']:6.3f}")
            print(f"  Min/Max:   {stats['min']:6.3f}  /  {stats['max']:6.3f}")
            print(f"  Q25/50/75: {stats['q25']:6.3f}  /  {stats['q50']:6.3f}  /  {stats['q75']:6.3f}")
    
    return summary
