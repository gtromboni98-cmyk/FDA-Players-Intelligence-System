"""
Base environment and application configuration.
Loads from .env file and provides core settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# API CREDENTIALS (REQUIRED)
# ============================================================================
CLIENT_ID = os.getenv("WYSCOUT_CLIENT_ID")
CLIENT_SECRET = os.getenv("WYSCOUT_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError(
        "Missing Wyscout API credentials!\n"
        "Please set environment variables in .env file:\n"
        "  WYSCOUT_CLIENT_ID=your_id\n"
        "  WYSCOUT_CLIENT_SECRET=your_secret"
    )

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ============================================================================
# DATA DIRECTORIES
# ============================================================================
CACHE_DIR = os.getenv("CACHE_DIR", "data/cache")
RAW_DATA_DIR = os.getenv("RAW_DATA_DIR", "data/raw")
PROCESSED_DATA_DIR = os.getenv("PROCESSED_DATA_DIR", "data/processed")

# ============================================================================
# API CONFIGURATION
# ============================================================================
API_BASE = os.getenv("API_BASE_URL")
API_TIMEOUT = int(os.getenv("API_TIMEOUT"))

# Optional settings with defaults
MAX_PLAYERS_PER_PAGE = int(os.getenv("MAX_PLAYERS_PER_PAGE", "100"))
REQUEST_RETRY_ATTEMPTS = int(os.getenv("REQUEST_RETRY_ATTEMPTS", "3"))
REQUEST_RETRY_DELAY = int(os.getenv("REQUEST_RETRY_DELAY", "2"))
