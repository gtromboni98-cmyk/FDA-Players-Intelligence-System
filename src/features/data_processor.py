"""
Data processing and preprocessing utilities.
"""

from typing import List, Dict, Optional, Tuple
import pandas as pd
from src.config import KNOWN_COMPETITIONS


class DataProcessor:
    """Handles data cleaning and preprocessing."""
    
    @staticmethod
    def create_players_dataframe(players_list: List[Dict]) -> pd.DataFrame:
        """
        Create a pandas DataFrame from player list.
        
        Args:
            players_list: List of player dictionaries
            
        Returns:
            DataFrame with player information
        """
        if not players_list:
            return pd.DataFrame()
        
        df = pd.DataFrame(players_list)
        
        # Data type conversions
        if 'birth_date' in df.columns:
            df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
        
        return df
    
    @staticmethod
    def filter_players_by_role(df: pd.DataFrame, roles: Optional[List[str]] = None) -> pd.DataFrame:
        """Filter players by their role."""
        if roles is None or 'role' not in df.columns:
            return df
        
        return df[df['role'].isin(roles)].copy()
    
    @staticmethod
    def filter_players_by_team(df: pd.DataFrame, team_names: Optional[List[str]] = None) -> pd.DataFrame:
        """Filter players by team name."""
        if team_names is None or 'team_name' not in df.columns:
            return df
        
        return df[df['team_name'].isin(team_names)].copy()
    
    @staticmethod
    def add_age_column(df: pd.DataFrame) -> pd.DataFrame:
        """Add age column based on birth date."""
        df = df.copy()
        
        if 'birth_date' not in df.columns:
            return df
        
        df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
        df['age'] = (pd.Timestamp.now() - df['birth_date']).dt.days // 365
        
        return df
    
    @staticmethod
    def handle_missing_data(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
        """
        Handle missing data in the dataframe.
        
        Args:
            df: Input dataframe
            strategy: 'drop' to remove nulls, 'fill' to fill with defaults
            
        Returns:
            Cleaned dataframe
        """
        df = df.copy()
        
        if strategy == 'drop':
            return df.dropna()
        elif strategy == 'fill':
            return df.fillna({
                'birth_date': 'Unknown',
                'role': 'Unknown',
                'team_name': 'Unknown'
            })
        
        return df
    
    @staticmethod
    def get_player_statistics(df: pd.DataFrame) -> Dict:
        """Calculate basic statistics about players."""
        stats = {
            'total_players': len(df),
            'unique_teams': df['team_name'].nunique() if 'team_name' in df.columns else 0,
            'unique_roles': df['role'].nunique() if 'role' in df.columns else 0,
        }
        
        if 'age' in df.columns:
            stats['avg_age'] = df['age'].mean()
            stats['min_age'] = df['age'].min()
            stats['max_age'] = df['age'].max()
        
        return stats


class CareerAnalyzer:
    """Analyzes player career data."""
    
    def __init__(self, team_id_to_name: Optional[Dict] = None):
        self.team_id_to_name = team_id_to_name or {}
        self.competition_id_to_name = {v: k for k, v in KNOWN_COMPETITIONS.items()}
    
    def filter_career_by_competitions(self, career_data: List[Dict], 
                                     competitions: Optional[List[str]] = None) -> List[Dict]:
        """
        Filter career data to specific competitions.
        
        Args:
            career_data: List of career entries
            competitions: Competition names to filter (None = no filter)
            
        Returns:
            Filtered career list
        """
        if not competitions:
            return career_data
        
        competition_ids = [KNOWN_COMPETITIONS.get(c) for c in competitions if c in KNOWN_COMPETITIONS]
        
        return [
            entry for entry in career_data
            if entry.get('competitionId') in competition_ids
        ]
    
    def enrich_career_data(self, career_data: List[Dict]) -> List[Dict]:
        """
        Enrich career data with human-readable names.
        
        Args:
            career_data: List of career entries
            
        Returns:
            Enriched career data with name mappings
        """
        enriched = []
        
        for entry in career_data:
            enriched_entry = entry.copy()
            
            # Add human-readable team name
            team_id = entry.get('teamId')
            if team_id:
                enriched_entry['team_name'] = self.team_id_to_name.get(team_id, 'Unknown Team')
            
            # Add human-readable competition name
            comp_id = entry.get('competitionId')
            if comp_id:
                enriched_entry['competition_name'] = self.competition_id_to_name.get(comp_id, 'Unknown')
            
            enriched.append(enriched_entry)
        
        return enriched
    
    def calculate_career_statistics(self, career_data: List[Dict]) -> Dict:
        """Calculate statistics from career data."""
        if not career_data:
            return {}
        
        total_appearances = sum(e.get('appearances', 0) for e in career_data)
        total_goals = sum(e.get('goal', 0) for e in career_data)
        total_minutes = sum(e.get('minutesPlayed', 0) for e in career_data)
        
        return {
            'total_appearances': total_appearances,
            'total_goals': total_goals,
            'total_minutes': total_minutes,
            'total_yellow_cards': sum(e.get('yellowCard', 0) for e in career_data),
            'total_red_cards': sum(e.get('redCards', 0) for e in career_data),
            'competitions_played': len(set(e.get('competitionId') for e in career_data if e.get('competitionId')))
        }
