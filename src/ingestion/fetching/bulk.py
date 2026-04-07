"""
Data fetching and collection module for player information.
"""

from typing import Dict, List, Set, Optional
from src.ingestion.api import WyscoutAPIClient
from src.config import KNOWN_COMPETITIONS, ACTIVE_COMPETITIONS


class DataFetcher:
    """Handles fetching and organizing player and team data."""
    
    def __init__(self, api_client: Optional[WyscoutAPIClient] = None):
        self.api_client = api_client or WyscoutAPIClient()
        self.teams_by_competition = {}
        self.team_id_to_name = {}
        self.season_id_to_name = {}
        self.competition_id_to_name = {v: k for k, v in KNOWN_COMPETITIONS.items()}
    
    def fetch_competitions_and_teams(self, exclude_primavera: bool = True) -> Dict[str, List[Dict]]:
        """
        Fetch all competitions and their teams.
        
        Args:
            exclude_primavera: If True, exclude Primavera from the results
            
        Returns:
            Dictionary with competition names as keys and team lists as values
        """
        competitions_list = self.api_client.fetch_competitions()
        if not competitions_list:
            print("Failed to fetch competitions")
            return {}
        
        for competition_name, wy_id in KNOWN_COMPETITIONS.items():
            if exclude_primavera and competition_name == 'Campionato Primavera 1':
                continue
            
            print(f"Fetching teams for {competition_name} (wyId: {wy_id})")
            teams = self.api_client.fetch_teams_by_competition(wy_id)
            
            if teams:
                self.teams_by_competition[competition_name] = teams
                # Build team_id_to_name map
                for team in teams:
                    team_wy_id = team.get('wyId')
                    if team_wy_id:
                        self.team_id_to_name[team_wy_id] = team.get('name', 'Unknown')
                print(f"  ✓ Successfully fetched {len(teams)} teams")
            else:
                print(f"  ✗ Failed to fetch teams")
        
        return self.teams_by_competition
    
    def fetch_squad_for_team(self, team_wy_id: int) -> List[Dict]:
        """Fetch all players in a team's squad."""
        team_players = []
        page = 1
        page_count = None
        
        print(f"Fetching players for team WyId: {team_wy_id}")
        
        while page_count is None or page <= page_count:
            data = self.api_client.fetch_players_by_team(team_wy_id, page)
            
            if not data:
                break
            
            squad = data.get('squad', [])
            for player in squad:
                full_name = f"{player.get('firstName', '')} {player.get('lastName', '')}".strip()
                team_players.append({
                    'name': full_name,
                    'wyId': player.get('wyId')
                })
            
            if page_count is None:
                page_count = data.get('pageCount', 1)
            
            page += 1
        
        print(f"  ✓ Fetched {len(team_players)} players")
        return team_players
    
    def fetch_player_details(self, player_wy_id: int) -> Optional[Dict]:
        """Fetch detailed information for a player."""
        player_data = self.api_client.fetch_player_details(player_wy_id)
        
        if not player_data:
            return None
        
        current_team_id = player_data.get('currentTeamId')
        current_team_name = self.team_id_to_name.get(current_team_id, 'Unknown Team')
        
        return {
            'shortName': player_data.get('shortName', 'N/A'),
            'birthDate': player_data.get('birthDate', 'N/A'),
            'currentTeam': current_team_name,
            'role': player_data.get('role', {}).get('name', 'N/A'),
            'currentTeamId': current_team_id
        }
    
    def fetch_player_career(self, player_wy_id: int, 
                          filter_competitions: Optional[List[str]] = None) -> Optional[List[Dict]]:
        """
        Fetch and optionally filter player career data.
        
        Args:
            player_wy_id: The player's Wyscout ID
            filter_competitions: List of competition names to filter by (None = no filter)
            
        Returns:
            List of career entries, filtered if requested
        """
        career_data = self.api_client.fetch_player_career(player_wy_id)
        
        if not career_data:
            return None
        
        if filter_competitions:
            competition_ids = [KNOWN_COMPETITIONS.get(comp) for comp in filter_competitions]
            career_data = [
                entry for entry in career_data
                if entry.get('competitionId') in competition_ids
            ]
        
        return career_data
    
    def fetch_all_players_from_competitions(self, competitions: Optional[List[str]] = None) -> List[Dict]:
        """
        Fetch all players from specified competitions.
        
        Args:
            competitions: List of competition names to fetch from. If None, uses ACTIVE_COMPETITIONS
            
        Returns:
            List of player dictionaries with full details
        """
        if competitions is None:
            competitions = list(ACTIVE_COMPETITIONS.keys())
        
        if not self.teams_by_competition:
            self.fetch_competitions_and_teams()
        
        all_players = []
        processed_player_ids: Set[int] = set()
        
        for competition_name in competitions:
            if competition_name not in self.teams_by_competition:
                print(f"Competition {competition_name} not available")
                continue
            
            print(f"\nProcessing {competition_name}...")
            teams = self.teams_by_competition[competition_name]
            
            for team in teams:
                team_wy_id = team.get('wyId')
                team_name = team.get('name')
                
                print(f"  Fetching players for {team_name}...")
                squad = self.fetch_squad_for_team(team_wy_id)
                
                for player_info in squad:
                    player_wy_id = player_info.get('wyId')
                    
                    if player_wy_id and player_wy_id not in processed_player_ids:
                        details = self.fetch_player_details(player_wy_id)
                        
                        if details:
                            all_players.append({
                                'name': player_info.get('name'),
                                'wyId': player_wy_id,
                                'team_name': team_name,
                                'birth_date': details.get('birthDate'),
                                'role': details.get('role')
                            })
                            processed_player_ids.add(player_wy_id)
        
        print(f"\n✓ Total unique players fetched: {len(all_players)}")
        return all_players
