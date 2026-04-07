"""
Ingestion module for fetching and processing raw data from APIs.
Organized as logical submodules: api, fetching.

BACKWARD COMPATIBILITY:
All ingestion components are re-exported here, so existing code like:
    from src.ingestion import WyscoutAPIClient, DataFetcher
will continue to work without modification.
"""

# ============================================================================
# API client
# ============================================================================
from .api import WyscoutAPIClient

# ============================================================================
# Data fetching
# ============================================================================
from .fetching import DataFetcher

__all__ = ['WyscoutAPIClient', 'DataFetcher']
