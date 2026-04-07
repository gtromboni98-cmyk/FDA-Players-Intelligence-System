"""
Analysis and modeling utilities for player intelligence system.
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np


class PlayerAnalyzer:
    """Analyzes and compares player performance metrics."""
    
    @staticmethod
    def find_similar_players(df: pd.DataFrame, target_player: Dict, 
                            n_similar: int = 5, 
                            features: Optional[List[str]] = None) -> List[Dict]:
        """
        Find players similar to a target player based on features.
        
        Args:
            df: DataFrame with player data
            target_player: Target player dictionary
            n_similar: Number of similar players to return
            features: Features to use for comparison (default: age, role)
            
        Returns:
            List of similar players
        """
        if features is None:
            features = ['age', 'role']
        
        # Filter available features
        available_features = [f for f in features if f in df.columns]
        
        if not available_features:
            return []
        
        df_compare = df.copy()
        
        # Match role if it's a feature
        if 'role' in available_features and 'role' in target_player:
            df_compare = df_compare[df_compare['role'] == target_player['role']]
        
        # If age is available, sort by age difference
        if 'age' in available_features and 'age' in target_player:
            df_compare['age_diff'] = abs(df_compare['age'] - target_player['age'])
            df_compare = df_compare.sort_values('age_diff')
        
        return df_compare.head(n_similar).to_dict('records')
    
    @staticmethod
    def rank_players(df: pd.DataFrame, metric: str, 
                    ascending: bool = False, top_n: Optional[int] = 10) -> pd.DataFrame:
        """
        Rank players by a specific metric.
        
        Args:
            df: DataFrame with player data
            metric: Column name to rank by
            ascending: If True, rank ascending (lower is better)
            top_n: Return top N players (None = all)
            
        Returns:
            Sorted DataFrame with rank column
        """
        if metric not in df.columns:
            raise ValueError(f"Metric '{metric}' not found in data")
        
        ranked = df.sort_values(metric, ascending=ascending).reset_index(drop=True)
        ranked['rank'] = range(1, len(ranked) + 1)
        
        if top_n:
            ranked = ranked.head(top_n)
        
        return ranked
    
    @staticmethod
    def calculate_percentiles(df: pd.DataFrame, column: str) -> pd.Series:
        """Calculate percentiles for a column."""
        return df[column].rank(pct=True) * 100


class CompetitionAnalyzer:
    """Analyzes competition-level data and statistics."""
    
    @staticmethod
    def get_team_player_count(df: pd.DataFrame) -> pd.DataFrame:
        """Get player count by team."""
        if 'team_name' not in df.columns:
            return pd.DataFrame()
        
        return df.groupby('team_name').size().reset_index(name='player_count').sort_values('player_count', ascending=False)
    
    @staticmethod
    def get_players_by_role(df: pd.DataFrame) -> pd.DataFrame:
        """Get player count by role."""
        if 'role' not in df.columns:
            return pd.DataFrame()
        
        return df.groupby('role').size().reset_index(name='count').sort_values('count', ascending=False)
    
    @staticmethod
    def get_age_statistics_by_team(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate age statistics grouped by team."""
        if 'team_name' not in df.columns or 'age' not in df.columns:
            return pd.DataFrame()
        
        return df.groupby('team_name')['age'].agg(['mean', 'min', 'max', 'std']).round(2).reset_index()
    
    @staticmethod
    def get_age_statistics_by_role(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate age statistics grouped by role."""
        if 'role' not in df.columns or 'age' not in df.columns:
            return pd.DataFrame()
        
        return df.groupby('role')['age'].agg(['mean', 'min', 'max', 'std']).round(2).reset_index()


class PerformanceScorer:
    """Scores players based on performance metrics."""
    
    @staticmethod
    def calculate_composite_score(series: pd.Series, weight: float = 1.0, 
                                 inverse: bool = False) -> pd.Series:
        """
        Calculate a normalized composite score from a series.
        
        Args:
            series: Input series of values
            weight: Weight to apply to the score
            inverse: If True, invert the score (for metrics where lower is better)
            
        Returns:
            Normalized scores (0-100)
        """
        # Normalize to 0-100
        min_val = series.min()
        max_val = series.max()
        
        if min_val == max_val:
            return pd.Series([50.0] * len(series), index=series.index)
        
        normalized = ((series - min_val) / (max_val - min_val)) * 100
        
        if inverse:
            normalized = 100 - normalized
        
        return normalized * weight
    
    @staticmethod
    def combine_scores(score_dict: Dict[str, Tuple[pd.Series, float]]) -> pd.Series:
        """
        Combine multiple scores with weights.
        
        Args:
            score_dict: Dictionary with score name -> (series, weight) tuples
            
        Returns:
            Combined weighted score
        """
        combined = pd.Series([0.0] * len(next(iter(score_dict.values()))[0]))
        total_weight = 0
        
        for name, (score, weight) in score_dict.items():
            combined += score * weight
            total_weight += weight
        
        return combined / total_weight if total_weight > 0 else combined
