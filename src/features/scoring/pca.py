"""
PCA-based player scoring system.
Implements 13-dimensional scoring for comprehensive player intelligence.
"""

from typing import List, Dict, Tuple, Optional
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from src.config import PCA_SCORE_DEFINITIONS, MIN_MINUTES_PLAYED


def get_pca_score_names() -> List[str]:
    """Get list of all available PCA score names."""
    return list(PCA_SCORE_DEFINITIONS.keys())


def get_score_features(score_name: str) -> List[str]:
    """
    Get the feature columns required for a specific PCA score.
    
    Args:
        score_name: Name of the PCA score
        
    Returns:
        List of feature column names
    """
    if score_name not in PCA_SCORE_DEFINITIONS:
        return []
    
    return PCA_SCORE_DEFINITIONS[score_name]['features']


def validate_features_exist(df: pd.DataFrame, features: List[str]) -> bool:
    """
    Check if all required features exist in the dataframe.
    
    Args:
        df: Input dataframe
        features: List of required features
        
    Returns:
        True if all features exist, False otherwise
    """
    return all(feature in df.columns for feature in features)


def calculate_single_pca_score(df: pd.DataFrame, score_name: str, 
                               features: Optional[List[str]] = None) -> Tuple[np.ndarray, PCA, StandardScaler]:
    """
    Calculate a single PCA score for all players.
    
    Process:
    1. Extract feature columns from dataframe
    2. Handle missing values (forward fill, then backward fill)
    3. Standardize features using StandardScaler
    4. Apply PCA with 1 component
    5. Normalize scores to [0, 1] range
    
    Args:
        df: Input dataframe with player data
        score_name: Name of the PCA score to calculate
        features: Optional override of feature list
        
    Returns:
        Tuple of (normalized_scores, pca_model, scaler)
        
    Raises:
        ValueError: If required features are missing
    """
    if features is None:
        features = get_score_features(score_name)
    
    if not features:
        raise ValueError(f"No features defined for score: {score_name}")
    
    # Validate features exist
    if not validate_features_exist(df, features):
        missing = [f for f in features if f not in df.columns]
        raise ValueError(f"Missing features for {score_name}: {missing}")
    
    # Extract feature data
    X = df[features].copy()
    
    # Handle missing values
    X = X.fillna(method='ffill').fillna(method='bfill').fillna(0)
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Apply PCA
    pca = PCA(n_components=1)
    pca_scores = pca.fit_transform(X_scaled).flatten()
    
    # Normalize to [0, 1]
    min_score = pca_scores.min()
    max_score = pca_scores.max()
    if max_score > min_score:
        normalized_scores = (pca_scores - min_score) / (max_score - min_score)
    else:
        normalized_scores = np.zeros_like(pca_scores)
    
    return normalized_scores, pca, scaler


def calculate_all_pca_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate all 13 PCA scores for the player dataframe.
    
    Scores calculated:
    1. DEFENSE_SCORE - Defensive actions (tackles, interceptions, blocks)
    2. PLAYMAKING - Ball progression (passes, key passes, pass accuracy)
    3. PROGRESSION - Forward play (progressive passes, through balls)
    4. FORWARD_ACTIVITY - Attacking (shots, dribbles, duration in final third)
    5. GOAL_THREAT - Finishing (xG, shots on target, goal conversion)
    6. SPEED_INTENSITY - Pace (pressures, high speed runs, displacement)
    7. POSSESSION_ACTIONS - Ball control (touches, passes, dribbles per touch)
    8. DUEL_SUCCESS - Physical (aerial wins, duel success %)
    9. CROSSING - Wide play (crosses, cross accuracy, assists from crosses)
    10. PENALTY_AREA - Box activity (actions in penalty area, shots from box)
    11. SET_PIECES - Set pieces (corner, free kick, throw-in events)
    12. CONSISTENCY - Game consistency (standard deviation in performance metrics)
    13. OVERALL - Weighted combination of all scores
    
    Args:
        df: Input dataframe with player statistics
        
    Returns:
        DataFrame with added PCA score columns
    """
    df_result = df.copy()
    
    # Calculate each PCA score
    for score_name in get_pca_score_names():
        if score_name == 'OVERALL':
            # Skip OVERALL for now, will compute after individual scores
            continue
        
        try:
            features = get_score_features(score_name)
            
            # Check if all features exist
            if not validate_features_exist(df_result, features):
                print(f"Warning: Skipping {score_name} - missing features")
                df_result[f'pca_{score_name}'] = np.nan
                continue
            
            # Calculate score
            scores, _, _ = calculate_single_pca_score(df_result, score_name, features)
            df_result[f'pca_{score_name}'] = scores
            
        except Exception as e:
            print(f"Error calculating {score_name}: {str(e)}")
            df_result[f'pca_{score_name}'] = np.nan
    
    # Calculate OVERALL score as weighted average
    score_columns = [col for col in df_result.columns if col.startswith('pca_') and col != 'pca_OVERALL']
    if score_columns:
        # Equal weights for all scores
        df_result['pca_OVERALL'] = df_result[score_columns].mean(axis=1)
    else:
        df_result['pca_OVERALL'] = np.nan
    
    return df_result


def aggregate_player_scores(df: pd.DataFrame, player_id_column: str = 'player_id') -> pd.DataFrame:
    """
    Aggregate PCA scores by player across multiple entries.
    
    Args:
        df: DataFrame with player scores
        player_id_column: Column containing player identifiers
        
    Returns:
        DataFrame with aggregated scores per player
    """
    score_columns = [col for col in df.columns if col.startswith('pca_')]
    
    if not score_columns:
        return df.groupby(player_id_column).first().reset_index()
    
    # Aggregate by player
    agg_dict = {col: 'mean' for col in score_columns}
    agg_dict['minutesPlayed'] = 'sum'
    
    # Add other columns that should be first value
    for col in df.columns:
        if col not in agg_dict and col != player_id_column:
            agg_dict[col] = 'first'
    
    result = df.groupby(player_id_column, as_index=False).agg(agg_dict)
    
    return result


def get_top_players_by_score(df: pd.DataFrame, score_name: str, n: int = 10, 
                            min_minutes: Optional[int] = None) -> pd.DataFrame:
    """
    Get top N players by a specific PCA score.
    
    Args:
        df: Player dataframe with PCA scores
        score_name: Name of the score to rank by
        n: Number of top players to return
        min_minutes: Minimum minutes played filter (default from config)
        
    Returns:
        Top players sorted by score
    """
    if min_minutes is None:
        min_minutes = MIN_MINUTES_PLAYED
    
    score_column = f'pca_{score_name}'
    
    if score_column not in df.columns:
        return pd.DataFrame()
    
    # Filter by minimum minutes
    filtered_df = df[df['minutesPlayed'] >= min_minutes].copy()
    
    # Sort by score descending
    top_players = filtered_df.nlargest(n, score_column)
    
    return top_players


def score_distribution_summary(df: pd.DataFrame) -> Dict[str, Dict]:
    """
    Generate summary statistics for all PCA scores.
    
    Args:
        df: Player dataframe with PCA scores
        
    Returns:
        Dictionary with distribution stats for each score
    """
    score_columns = [col for col in df.columns if col.startswith('pca_')]
    
    summary = {}
    
    for score_col in score_columns:
        score_name = score_col.replace('pca_', '')
        
        # Remove NaN values for calculation
        valid_scores = df[score_col].dropna()
        
        if len(valid_scores) > 0:
            summary[score_name] = {
                'mean': float(valid_scores.mean()),
                'std': float(valid_scores.std()),
                'min': float(valid_scores.min()),
                'max': float(valid_scores.max()),
                'median': float(valid_scores.median()),
                'q25': float(valid_scores.quantile(0.25)),
                'q75': float(valid_scores.quantile(0.75)),
                'count': len(valid_scores),
                'nan_count': df[score_col].isna().sum()
            }
        else:
            summary[score_name] = {'count': 0, 'nan_count': len(df)}
    
    return summary
