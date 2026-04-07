"""
Ingestion module for fetching and processing raw data from APIs.
"""

from .api_client import WyscoutAPIClient
from .data_fetcher import DataFetcher

__all__ = ['WyscoutAPIClient', 'DataFetcher']
