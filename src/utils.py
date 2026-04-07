"""
Utility functions for data persistence and file handling.
"""

import os
import pickle
import json
from typing import Any, Dict, Optional
import pandas as pd
from src.config import CACHE_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR


class DataManager:
    """Manages data persistence and loading."""
    
    @staticmethod
    def ensure_directories():
        """Create necessary data directories if they don't exist."""
        for directory in [CACHE_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR]:
            os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def save_pickle(data: Any, filepath: str):
        """Save data as pickle file."""
        DataManager.ensure_directories()
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"✓ Data saved to {filepath}")
    
    @staticmethod
    def load_pickle(filepath: str) -> Optional[Any]:
        """Load data from pickle file."""
        if not os.path.exists(filepath):
            print(f"✗ File not found: {filepath}")
            return None
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        print(f"✓ Data loaded from {filepath}")
        return data
    
    @staticmethod
    def save_dataframe(df: pd.DataFrame, filepath: str, fmt: str = 'csv'):
        """
        Save DataFrame to file.
        
        Args:
            df: DataFrame to save
            filepath: Output filepath
            fmt: Format - 'csv', 'pickle', 'parquet', 'excel'
        """
        DataManager.ensure_directories()
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        
        if fmt == 'csv':
            df.to_csv(filepath, index=False)
        elif fmt == 'pickle':
            df.to_pickle(filepath)
        elif fmt == 'parquet':
            df.to_parquet(filepath, index=False)
        elif fmt == 'excel':
            df.to_excel(filepath, index=False)
        else:
            raise ValueError(f"Unknown format: {fmt}")
        
        print(f"✓ DataFrame saved to {filepath}")
    
    @staticmethod
    def load_dataframe(filepath: str) -> Optional[pd.DataFrame]:
        """Load DataFrame from file (auto-detects format)."""
        if not os.path.exists(filepath):
            print(f"✗ File not found: {filepath}")
            return None
        
        ext = os.path.splitext(filepath)[1].lower()
        
        try:
            if ext == '.csv':
                df = pd.read_csv(filepath)
            elif ext == '.xlsx':
                df = pd.read_excel(filepath)
            elif ext == '.parquet':
                df = pd.read_parquet(filepath)
            elif ext == '.pkl':
                df = pd.read_pickle(filepath)
            else:
                print(f"✗ Unknown file format: {ext}")
                return None
            
            print(f"✓ DataFrame loaded from {filepath}")
            return df
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            return None
    
    @staticmethod
    def save_json(data: Dict, filepath: str):
        """Save dictionary as JSON file."""
        DataManager.ensure_directories()
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ JSON saved to {filepath}")
    
    @staticmethod
    def load_json(filepath: str) -> Optional[Dict]:
        """Load JSON file."""
        if not os.path.exists(filepath):
            print(f"✗ File not found: {filepath}")
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"✓ JSON loaded from {filepath}")
        return data


class Logger:
    """Simple logging utility."""
    
    @staticmethod
    def print_section(title: str, char: str = "="):
        """Print a formatted section header."""
        print(f"\n{char * 60}")
        print(f"  {title}")
        print(f"{char * 60}\n")
    
    @staticmethod
    def print_success(message: str):
        """Print success message."""
        print(f"✓ {message}")
    
    @staticmethod
    def print_error(message: str):
        """Print error message."""
        print(f"✗ {message}")
    
    @staticmethod
    def print_info(message: str):
        """Print info message."""
        print(f"ℹ {message}")
