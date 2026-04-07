"""
Position mapping and generalization utilities.
"""

from typing import List, Dict, Optional, Tuple
import pandas as pd
from src.config import POSITION_MAPPING


def generalize_position(position: str) -> Optional[str]:
    """
    Map a specific position to a generalized role.
    
    Args:
        position: Specific position string
        
    Returns:
        Generalized role or None if not found
    """
    return POSITION_MAPPING.get(position)


def generalize_position_from_list(positions: List[str]) -> Optional[str]:
    """
    Generalize position from a list (use first valid generalization).
    
    Args:
        positions: List of position strings
        
    Returns:
        Generalized role or None if none found
    """
    for pos in positions:
        generalized = generalize_position(pos)
        if generalized:
            return generalized
    return None


def apply_position_mapping(df: pd.DataFrame, position_column: str = 'position') -> pd.DataFrame:
    """
    Apply position mapping to a dataframe.
    
    Args:
        df: DataFrame containing position data
        position_column: Column name containing positions
        
    Returns:
        DataFrame with added 'generalized_position' column
    """
    df = df.copy()
    
    if position_column not in df.columns:
        df['generalized_position'] = None
        return df
    
    df['generalized_position'] = df[position_column].apply(generalize_position)
    
    return df


def get_available_positions() -> Dict[str, str]:
    """Get all available position mappings."""
    return POSITION_MAPPING.copy()


def filter_by_position(df: pd.DataFrame, positions: List[str], 
                      position_column: str = 'generalized_position') -> pd.DataFrame:
    """
    Filter dataframe by specific positions.
    
    Args:
        df: Input dataframe
        positions: List of positions to filter
        position_column: Column to filter on
        
    Returns:
        Filtered dataframe
    """
    if position_column not in df.columns:
        return df
    
    return df[df[position_column].isin(positions)].copy()


def get_position_distribution(df: pd.DataFrame, position_column: str = 'generalized_position') -> Dict[str, int]:
    """
    Get distribution of positions in dataframe.
    
    Args:
        df: Input dataframe
        position_column: Column to analyze
        
    Returns:
        Dictionary with position counts
    """
    if position_column not in df.columns:
        return {}
    
    distribution = df[position_column].value_counts().to_dict()
    return distribution
