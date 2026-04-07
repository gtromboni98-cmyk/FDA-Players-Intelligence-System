"""
API client module for fetching data from Wyscout API.
"""

import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, List, Optional, Any
from src.config import CLIENT_ID, CLIENT_SECRET, ENDPOINTS, API_TIMEOUT


class WyscoutAPIClient:
    """Client for interacting with the Wyscout API."""
    
    def __init__(self, client_id: str = CLIENT_ID, client_secret: str = CLIENT_SECRET, timeout: int = API_TIMEOUT):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth = HTTPBasicAuth(client_id, client_secret)
        self.timeout = timeout
    
    def _make_request(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Make a GET request to the API.
        
        Args:
            url: The full URL to request
            
        Returns:
            JSON response as dictionary or None if request fails
        """
        try:
            response = requests.get(url, auth=self.auth, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
    
    def fetch_competitions(self, area_id: str = "ITA") -> Optional[List[Dict]]:
        """Fetch competitions for a specific area."""
        url = f"{ENDPOINTS['competitions_area']}"
        data = self._make_request(url)
        return data.get('competitions') if data else None
    
    def fetch_teams_by_competition(self, competition_wy_id: int) -> Optional[List[Dict]]:
        """Fetch teams for a specific competition."""
        url = ENDPOINTS['squad_list'].format(wyId=competition_wy_id)
        data = self._make_request(url)
        return data.get('teams') if data else None
    
    def fetch_players_by_team(self, team_wy_id: int, page: int = 1) -> Optional[Dict]:
        """Fetch players (squad) for a specific team."""
        url = f"{ENDPOINTS['players_by_team'].format(team_wyId=team_wy_id)}?page={page}"
        data = self._make_request(url)
        return data
    
    def fetch_paginated_data(self, url: str, data_field: str) -> List[Dict]:
        """
        Fetch data with pagination support.
        
        Args:
            url: The base URL template (without pagination)
            data_field: The field name in the response containing the data
            
        Returns:
            List of all items from all pages
        """
        all_items = []
        page = 1
        page_count = None
        
        while page_count is None or page <= page_count:
            current_url = f"{url}?page={page}"
            data = self._make_request(current_url)
            
            if not data:
                break
            
            items = data.get(data_field, [])
            all_items.extend(items)
            
            if page_count is None:
                page_count = data.get('pageCount', 1)
            
            page += 1
        
        return all_items
    
    def fetch_player_career(self, player_wy_id: int) -> Optional[List[Dict]]:
        """Fetch career history for a player."""
        url = ENDPOINTS['player_career'].format(wyId=player_wy_id)
        data = self._make_request(url)
        return data.get('career') if data else None
    
    def fetch_player_details(self, player_wy_id: int) -> Optional[Dict]:
        """Fetch detailed information about a player."""
        url = ENDPOINTS['player_details'].format(wyId=player_wy_id)
        return self._make_request(url)
    
    def fetch_season_details(self, season_wy_id: int) -> Optional[Dict]:
        """Fetch details about a season."""
        url = ENDPOINTS['seasons'].format(wyId=season_wy_id)
        return self._make_request(url)
    
    def fetch_player_advanced_stats(self, player_wy_id: int, page: int = 1) -> Optional[Dict]:
        """Fetch advanced statistics for a player."""
        url = f"{ENDPOINTS['player_advanced_stats'].format(wyId=player_wy_id)}?page={page}"
        return self._make_request(url)
    
    def fetch_player_matches(self, player_wy_id: int, page: int = 1) -> Optional[Dict]:
        """Fetch match history for a player."""
        url = f"{ENDPOINTS['player_matches'].format(wyId=player_wy_id)}?page={page}"
        return self._make_request(url)
