"""
Match statistics expansion and extraction utilities.
"""

from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np


def extract_total_stats(stats_dict: Optional[Dict]) -> Dict:
    """
    Extract total statistics from stats dictionary.
    
    Args:
        stats_dict: Statistics dictionary from API
        
    Returns:
        Dictionary with total stats (goals, assists, yellowCard, redCards, etc.)
    """
    if not stats_dict:
        return {}
    
    result = {}
    
    for key in ['goals', 'ownGoals', 'assists', 'yellowCard', 'redCards', 'keyPasses']:
        value = stats_dict.get(key)
        if value is not None:
            result[f'total_{key}'] = value
    
    return result


def extract_average_stats(stats_dict: Optional[Dict]) -> Dict:
    """
    Extract average statistics per match.
    
    Args:
        stats_dict: Statistics dictionary from API
        
    Returns:
        Dictionary with averaged stats
    """
    if not stats_dict:
        return {}
    
    result = {}
    
    # Average per 90 minutes statistics
    average_keys = ['goals', 'assists', 'passes', 'shots', 'dribbles', 
                   'tackles', 'interceptions', 'passAccuracy', 'keyPasses']
    
    for key in average_keys:
        value = stats_dict.get(f'{key}PerMatch')
        if value is not None:
            result[f'avg_{key}'] = value
    
    # Handle rate-based stats (already averaged or percentage)
    if 'passAccuracy' in stats_dict:
        result['avg_pass_accuracy'] = stats_dict['passAccuracy']
    
    return result


def expand_match_stats(df: pd.DataFrame, stats_column: str = 'stats') -> pd.DataFrame:
    """
    Expand nested statistics dictionary into separate columns.
    
    Args:
        df: DataFrame with nested stats
        stats_column: Column containing stats dictionaries
        
    Returns:
        DataFrame with flattened statistics columns
    """
    df = df.copy()
    
    if stats_column not in df.columns:
        return df
    
    # Extract total and average stats
    total_stats_list = []
    average_stats_list = []
    
    for stats in df[stats_column]:
        total = extract_total_stats(stats)
        average = extract_average_stats(stats)
        
        # Merge total and average
        combined = {**total, **average}
        total_stats_list.append(total)
        average_stats_list.append(average)
    
    # Create dataframes from lists
    total_stats_df = pd.DataFrame(total_stats_list)
    average_stats_df = pd.DataFrame(average_stats_list)
    
    # Concatenate with original dataframe
    result = pd.concat([df, total_stats_df, average_stats_df], axis=1)
    
    return result


def extract_positions_from_nested(positions_data: Optional[List[Dict]]) -> Dict[str, int]:
    """
    Extract position information from nested position data.
    
    Args:
        positions_data: List of position dictionaries
        
    Returns:
        Dictionary mapping position names to counts
    """
    if not positions_data:
        return {}
    
    position_counts = {}
    
    for pos_info in positions_data:
        if isinstance(pos_info, dict):
            position = pos_info.get('position')
            appearances = pos_info.get('appearances', 1)
            
            if position:
                position_counts[position] = position_counts.get(position, 0) + appearances
    
    return position_counts


def clean_match_stats_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize match statistics dataframe.
    
    Args:
        df: Statistics dataframe with potential nested/mixed data
        
    Returns:
        Cleaned dataframe
    """
    df = df.copy()
    
    # Fill NaN values in numeric columns with 0
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    # Fill NaN values in string columns with 'Unknown'
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        if col not in ['stats', 'positions', 'positionString']:  # Don't fill nested structures
            df[col] = df[col].fillna('Unknown')
    
    # Remove duplicate columns if any
    df = df.loc[:, ~df.columns.duplicated()]
    
    # Ensure numeric stats are float type
    stats_columns = [col for col in df.columns if col.startswith(('total_', 'avg_'))]
    for col in stats_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df
