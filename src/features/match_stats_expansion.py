"""
Match statistics expansion and feature extraction utilities.
Extracts nested fields from API responses into separate columns.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


def extract_total_stats(total_stats_dict: Dict) -> Dict:
    """
    Extracts key statistics from the 'total' nested field.
    
    Args:
        total_stats_dict: Dictionary from API response 'total' field
        
    Returns:
        Dictionary with extracted statistics
    """
    if not isinstance(total_stats_dict, dict):
        return {}
    
    return {
        'minutesOnField': total_stats_dict.get('minutesOnField', 0),
        'goals': total_stats_dict.get('goals', 0),
        'assists': total_stats_dict.get('assists', 0),
        'yellowCards': total_stats_dict.get('yellowCards', 0),
        'redCards': total_stats_dict.get('redCards', 0),
        'penalties': total_stats_dict.get('penalties', 0),
        'corners': total_stats_dict.get('corners', 0),
        'pressingDuels': total_stats_dict.get('pressingDuels', 0),
        'pressingDuelsWon': total_stats_dict.get('pressingDuelsWon', 0)
    }


def extract_average_stats(average_stats_dict: Dict) -> Dict:
    """
    Extracts comprehensive statistics from the 'average' nested field.
    Per 90 or per-match averages.
    
    Args:
        average_stats_dict: Dictionary from API response 'average' field
        
    Returns:
        Dictionary with 45+ extracted statistics
    """
    if not isinstance(average_stats_dict, dict):
        return {}
    
    return {
        # Duels & Battles
        'duels': average_stats_dict.get('duels', 0),
        'duelsWon_percent': average_stats_dict.get('duelsWon', 0),
        'defensiveDuels': average_stats_dict.get('defensiveDuels', 0),
        'defensiveDuelsWon_percent': average_stats_dict.get('defensiveDuelsWon', 0),
        'offensiveDuels': average_stats_dict.get('offensiveDuels', 0),
        'offensiveDuelsWon_percent': average_stats_dict.get('offensiveDuelsWon', 0),
        'aerialDuels': average_stats_dict.get('aerialDuels', 0),
        'aerialDuelsWon_percent': average_stats_dict.get('aerialDuelsWon', 0),
        
        # Defensive
        'defensiveActions': average_stats_dict.get('defensiveActions', 0),
        'interceptions': average_stats_dict.get('interceptions', 0),
        'clearances': average_stats_dict.get('clearances', 0),
        'slidingTackles': average_stats_dict.get('slidingTackles', 0),
        'successfulSlidingTackles_percent': average_stats_dict.get('successfulSlidingTackles', 0),
        'shotsBlocked': average_stats_dict.get('shotsBlocked', 0),
        'ballRecoveries': average_stats_dict.get('ballRecoveries', 0),
        'dribblesAgainst': average_stats_dict.get('dribblesAgainst', 0),
        'dribblesAgainstWon_percent': average_stats_dict.get('dribblesAgainstWon', 0),
        'looseBallDuels': average_stats_dict.get('looseBallDuels', 0),
        'looseBallDuelsWon': average_stats_dict.get('looseBallDuelsWon', 0),
        'counterpressingRecoveries': average_stats_dict.get('counterpressingRecoveries', 0),
        'fouls': average_stats_dict.get('fouls', 0),
        'foulsSuffered': average_stats_dict.get('foulsSuffered', 0),
        'missedBalls': average_stats_dict.get('missedBalls', 0),
        
        # Passing
        'passes': average_stats_dict.get('passes', 0),
        'successfulPasses_percent': average_stats_dict.get('successfulPasses', 0),
        'passLength': average_stats_dict.get('passLength', 0),
        'longPassLength': average_stats_dict.get('longPassLength', 0),
        'forwardPasses': average_stats_dict.get('forwardPasses', 0),
        'successfulForwardPasses_percent': average_stats_dict.get('successfulForwardPasses', 0),
        'backPasses': average_stats_dict.get('backPasses', 0),
        'successfulBackPasses_percent': average_stats_dict.get('successfulBackPasses', 0),
        'verticalPasses': average_stats_dict.get('verticalPasses', 0),
        'successfulVerticalPasses_percent': average_stats_dict.get('successfulVerticalPasses', 0),
        'longPasses': average_stats_dict.get('longPasses', 0),
        'successfulLongPasses_percent': average_stats_dict.get('successfulLongPasses', 0),
        'lateralPasses': average_stats_dict.get('lateralPasses', 0),
        'successfulLateralPasses_percent': average_stats_dict.get('successfulLateralPasses', 0),
        'smartPasses': average_stats_dict.get('smartPasses', 0),
        'successfulSmartPasses_percent': average_stats_dict.get('successfulSmartPasses', 0),
        'passesToFinalThird': average_stats_dict.get('passesToFinalThird', 0),
        'successfulPassesToFinalThird_percent': average_stats_dict.get('successfulPassesToFinalThird', 0),
        'keyPasses': average_stats_dict.get('keyPasses', 0),
        'successfulKeyPasses_percent': average_stats_dict.get('successfulKeyPasses', 0),
        'throughPasses': average_stats_dict.get('throughPasses', 0),
        'successfulThroughPasses_percent': average_stats_dict.get('successfulThroughPasses', 0),
        'progressivePasses': average_stats_dict.get('progressivePasses', 0),
        'successfulProgressivePasses_percent': average_stats_dict.get('successfulProgressivePasses', 0),
        
        # Dribbling & Movement
        'dribbles': average_stats_dict.get('dribbles', 0),
        'successfulDribbles_percent': average_stats_dict.get('successfulDribbles', 0),
        'accelerations': average_stats_dict.get('accelerations', 0),
        'progressiveRun': average_stats_dict.get('progressiveRun', 0),
        'dribbleDistanceFromOpponentGoal': average_stats_dict.get('dribbleDistanceFromOpponentGoal', 0),
        'crosses': average_stats_dict.get('crosses', 0),
        'successfulCrosses_percent': average_stats_dict.get('successfulCrosses', 0),
        
        # Shooting
        'shots': average_stats_dict.get('shots', 0),
        'shotsOnTarget_percent': average_stats_dict.get('shotsOnTarget', 0),
        'headShots': average_stats_dict.get('headShots', 0),
        'headShotsOnTarget_percent': average_stats_dict.get('headShotsOnTarget', 0),
        'goalConversion_percent': average_stats_dict.get('goalConversion', 0),
        'directFreeKicksOnTarget_percent': average_stats_dict.get('directFreeKicksOnTarget', 0),
        'xgShot': average_stats_dict.get('xgShot', 0),
        
        # Playmaking
        'shotAssists': average_stats_dict.get('shotAssists', 0),
        'successfulShotAssists_percent': average_stats_dict.get('successfulShotAssists', 0),
        'shotOnTargetAssists': average_stats_dict.get('shotOnTargetAssists', 0),
        'xgAssist': average_stats_dict.get('xgAssist', 0),
        'secondAssists': average_stats_dict.get('secondAssists', 0),
        'thirdAssists': average_stats_dict.get('thirdAssists', 0),
        
        # Recovery & Losses
        'ballLosses': average_stats_dict.get('ballLosses', 0),
        'losses': average_stats_dict.get('losses', 0),
        'ownHalfLosses': average_stats_dict.get('ownHalfLosses', 0),
        'dangerousOwnHalfLosses': average_stats_dict.get('dangerousOwnHalfLosses', 0),
        'opponentHalfRecoveries': average_stats_dict.get('opponentHalfRecoveries', 0),
        'dangerousOpponentHalfRecoveries': average_stats_dict.get('dangerousOpponentHalfRecoveries', 0),
        
        # Attacking Context
        'attackingActions': average_stats_dict.get('attackingActions', 0),
        'linkupPlays': average_stats_dict.get('linkupPlays', 0),
        'successfulLinkupPlays_percent': average_stats_dict.get('successfulLinkupPlays', 0),
        'touchInBox': average_stats_dict.get('touchInBox', 0),
        'receivedPass': average_stats_dict.get('receivedPass', 0),
        'offsides': average_stats_dict.get('offsides', 0),
    }


def expand_match_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expands nested 'total', 'average', and 'percent' columns into separate feature columns.
    
    Args:
        df: DataFrame with nested stats (from API response)
        
    Returns:
        DataFrame with expanded columns, original nested columns dropped
    """
    df = df.copy()
    
    # Extract total stats
    if 'total' in df.columns:
        total_expanded = df['total'].apply(extract_total_stats).apply(pd.Series)
        df = pd.concat([df, total_expanded], axis=1)
    
    # Extract average stats
    if 'average' in df.columns:
        average_expanded = df['average'].apply(extract_average_stats).apply(pd.Series)
        df = pd.concat([df, average_expanded], axis=1)
    
    # Drop original nested columns
    columns_to_drop = [col for col in ['total', 'average', 'percent'] if col in df.columns]
    df = df.drop(columns=columns_to_drop)
    
    return df


def extract_positions_from_nested(positions_list: List[Dict]) -> Optional[str]:
    """
    Extracts position names from nested positions array.
    
    Args:
        positions_list: List of position dictionaries from API
        
    Returns:
        Comma-separated position names, or None
    """
    if not isinstance(positions_list, list) or not positions_list:
        return None
    
    position_names = []
    for pos_dict in positions_list:
        if isinstance(pos_dict, dict) and 'position' in pos_dict:
            pos_name = pos_dict['position'].get('name')
            if pos_name:
                position_names.append(pos_name)
    
    return ', '.join(position_names) if position_names else None


def clean_match_stats_df(df: pd.DataFrame, min_minutes: int = 10) -> pd.DataFrame:
    """
    Cleans match statistics DataFrame:
    - Removes entries with < min_minutes played
    - Handles missing values
    - Standardizes data types
    
    Args:
        df: DataFrame with match stats
        min_minutes: Minimum minutes threshold
        
    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    
    # Filter by minutes played
    if 'minutesOnField' in df.columns:
        initial_count = len(df)
        df = df[df['minutesOnField'] >= min_minutes]
        removed_count = initial_count - len(df)
        print(f"Removed {removed_count} entries with < {min_minutes} minutes played")
    
    # Fill NaN values with 0 for numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    return df
