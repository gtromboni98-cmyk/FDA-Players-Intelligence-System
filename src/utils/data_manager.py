"""
Data management utilities for file persistence and loading.
Supports pickle, CSV, JSON, Parquet, and Excel formats.
"""

import os
import pickle
import json
from typing import Any, Dict, Optional, Union
from pathlib import Path
import pandas as pd

from src.config import CACHE_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR


class DataManager:
    """Manages data persistence and loading across multiple formats."""
    
    @staticmethod
    def ensure_directories():
        """Create necessary data directories if they don't exist."""
        for directory in [CACHE_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR]:
            os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def save_pickle(data: Any, filepath: Union[str, Path]):
        """
        Save data as pickle file.
        
        Args:
            data: Data to save
            filepath: Path where to save the file
        """
        filepath = Path(filepath)
        DataManager.ensure_directories()
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    @staticmethod
    def load_pickle(filepath: Union[str, Path]) -> Optional[Any]:
        """
        Load data from pickle file.
        
        Args:
            filepath: Path to pickle file
            
        Returns:
            Loaded data or None if file not found
        """
        filepath = Path(filepath)
        if not filepath.exists():
            return None
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        return data
    
    @staticmethod
    def save_dataframe(df: pd.DataFrame, filepath: Union[str, Path], fmt: str = 'pkl'):
        """
        Save DataFrame to file in specified format.
        
        Args:
            df: DataFrame to save
            filepath: Output filepath
            fmt: Format - 'csv', 'pkl', 'parquet', 'xlsx'
        """
        filepath = Path(filepath)
        DataManager.ensure_directories()
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        if fmt in ['pkl', 'pickle']:
            df.to_pickle(filepath)
        elif fmt == 'csv':
            df.to_csv(filepath, index=False)
        elif fmt == 'parquet':
            df.to_parquet(filepath, index=False)
        elif fmt in ['xlsx', 'excel']:
            df.to_excel(filepath, index=False)
        else:
            raise ValueError(f"Unknown format: {fmt}")
    
    @staticmethod
    def load_dataframe(filepath: Union[str, Path]) -> Optional[pd.DataFrame]:
        """
        Load DataFrame from file (auto-detects format from extension).
        
        Args:
            filepath: Path to data file
            
        Returns:
            Loaded DataFrame or None if file not found
        """
        filepath = Path(filepath)
        if not filepath.exists():
            return None
        
        ext = filepath.suffix.lower()
        
        try:
            if ext == '.csv':
                df = pd.read_csv(filepath)
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(filepath)
            elif ext == '.parquet':
                df = pd.read_parquet(filepath)
            elif ext in ['.pkl', '.pickle']:
                df = pd.read_pickle(filepath)
            else:
                return None
            
            return df
        except Exception as e:
            return None
    
    @staticmethod
    def save_json(data: Dict, filepath: Union[str, Path]):
        """
        Save dictionary as JSON file.
        
        Args:
            data: Dictionary to save
            filepath: Output filepath
        """
        filepath = Path(filepath)
        DataManager.ensure_directories()
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_json(filepath: Union[str, Path]) -> Optional[Dict]:
        """
        Load JSON file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Loaded dictionary or None if file not found
        """
        filepath = Path(filepath)
        if not filepath.exists():
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
