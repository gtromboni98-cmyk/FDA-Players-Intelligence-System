"""
Position mapping and categorization utilities.
Maps detailed position names to 9 generalized roles.
"""

import pandas as pd
from typing import Optional, List, Set
from src.config import POSITION_MAPPING


def generalize_position(detailed_position: str) -> str:
    """
    Maps a detailed position to a generalized role.
    
    Args:
        detailed_position: Detailed position name from Wyscout API
        
    Returns:
        Generalized position name, or 'Unknown' if not found
    """
    if pd.isna(detailed_position) or not isinstance(detailed_position, str):
        return 'Unknown'
    
    position = detailed_position.strip()
    return POSITION_MAPPING.get(position, 'Unknown')


def generalize_position_from_list(positions_str: str) -> str:
    """
    Maps comma-separated detailed positions to a single generalized role.
    Uses the first position if multiple are provided.
    
    Args:
        positions_str: Comma-separated position names
        
    Returns:
        Generalized position name
    """
    if pd.isna(positions_str) or not isinstance(positions_str, str):
        return 'Unknown'
    
    # Split by comma and process each position
    individual_positions = [p.strip() for p in positions_str.split(',')]
    
    # Get mappings for each position
    generalized_roles = []
    for pos in individual_positions:
        mapped_pos = generalize_position(pos)
        if mapped_pos != 'Unknown':
            generalized_roles.append(mapped_pos)
    
    # Return the first generalized role if any found
    if generalized_roles:
        return generalized_roles[0]
    
    return 'Unknown'


def apply_position_mapping(df: pd.DataFrame, position_column: str = 'positions') -> pd.DataFrame:
    """
    Applies position mapping to a DataFrame.
    Adds a new 'generalized_position' column and optionally replaces the original.
    
    Args:
        df: DataFrame with position column
        position_column: Name of the column containing detailed positions
        
    Returns:
        DataFrame with 'generalized_position' column added
    """
    df = df.copy()
    
    if position_column not in df.columns:
        raise ValueError(f"Column '{position_column}' not found in DataFrame")
    
    # Apply mapping
    df['generalized_position'] = df[position_column].apply(generalize_position_from_list)
    
    return df


def get_available_positions() -> List[str]:
    """
    Returns the list of 9 generalized positions.
    
    Returns:
        Sorted list of generalized position names
    """
    return sorted(list(set(POSITION_MAPPING.values())))


def filter_by_position(df: pd.DataFrame, position: str, position_column: str = 'positions') -> pd.DataFrame:
    """
    Filters DataFrame to only include players in a specific generalized position.
    
    Args:
        df: DataFrame with position data
        position: Generalized position to filter by
        position_column: Name of the column containing positions
        
    Returns:
        Filtered DataFrame
    """
    if 'generalized_position' not in df.columns:
        df = apply_position_mapping(df, position_column)
    
    return df[df['generalized_position'] == position].copy()


def get_position_distribution(df: pd.DataFrame, position_column: str = 'positions') -> pd.Series:
    """
    Returns the distribution of positions in the DataFrame.
    
    Args:
        df: DataFrame with position data
        position_column: Name of the column containing positions
        
    Returns:
        Series with position counts
    """
    if 'generalized_position' not in df.columns:
        df = apply_position_mapping(df, position_column)
    
    return df['generalized_position'].value_counts()
