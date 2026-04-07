"""
Script 07: Match Statistics Expansion
Expands nested API response fields into separate feature columns.
Input:  data/raw/match_stats.pkl (from script 06)
Output: data/processed/match_stats_expanded.pkl
"""

import sys
import pickle
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.features.match_stats_expansion import (
    expand_match_stats, 
    extract_positions_from_nested,
    clean_match_stats_df
)
from src.utils import Logger

logger = Logger(__name__)


def run_match_stats_expansion():
    """
    Main execution function.
    1. Load raw match stats from pickle
    2. Expand nested JSON fields (total, average, percent)
    3. Extract positions array
    4. Clean and validate data
    5. Save expanded stats
    """
    
    logger.info("=" * 80)
    logger.info("SCRIPT 07: Match Statistics Expansion")
    logger.info("=" * 80)
    
    # Load raw match stats
    match_stats_path = Path('data/raw/match_stats.pkl')
    if not match_stats_path.exists():
        logger.error(f"❌ File not found: {match_stats_path}")
        logger.error("   Please run script 06 first to fetch match statistics")
        return False
    
    try:
        with open(match_stats_path, 'rb') as f:
            match_stats = pickle.load(f)
        logger.info(f"✅ Loaded {len(match_stats)} match records from {match_stats_path}")
    except Exception as e:
        logger.error(f"❌ Error loading {match_stats_path}: {e}")
        return False
    
    # Convert to DataFrame if needed
    if not isinstance(match_stats, pd.DataFrame):
        match_stats = pd.DataFrame(match_stats)
    
    logger.info(f"   DataFrame shape: {match_stats.shape}")
    logger.info(f"   Columns: {list(match_stats.columns)}")
    
    # Expand nested fields
    logger.info("\n📊 Expanding nested fields...")
    try:
        match_stats_expanded = expand_match_stats(match_stats)
        logger.info(f"✅ Expanded to {match_stats_expanded.shape[1]} total columns")
        logger.info(f"   New columns: {list(match_stats_expanded.columns)}")
    except Exception as e:
        logger.error(f"❌ Error expanding nested fields: {e}")
        return False
    
    # Extract positions from nested array (if exists)
    if 'positions' in match_stats_expanded.columns:
        logger.info("\n📍 Extracting positions from nested array...")
        try:
            match_stats_expanded['position'] = match_stats_expanded['positions'].apply(
                extract_positions_from_nested
            )
            match_stats_expanded = match_stats_expanded.drop(columns=['positions'])
            logger.info(f"✅ Positions extracted and saved to 'position' column")
        except Exception as e:
            logger.warning(f"⚠️  Could not extract positions: {e}")
    
    # Clean and validate
    logger.info("\n🧹 Cleaning data...")
    initial_count = len(match_stats_expanded)
    match_stats_expanded = clean_match_stats_df(match_stats_expanded, min_minutes=10)
    removed_count = initial_count - len(match_stats_expanded)
    logger.info(f"   Removed {removed_count} entries with < 10 minutes")
    
    # Handle missing values
    numeric_cols = match_stats_expanded.select_dtypes(include=['number']).columns
    logger.info(f"\n📋 Data quality check:")
    logger.info(f"   Numeric columns: {len(numeric_cols)}")
    missing_values = match_stats_expanded.isna().sum()
    if missing_values.sum() > 0:
        logger.warning(f"   Missing values found (will be filled with 0)")
        logger.warning(f"   {missing_values[missing_values > 0]}")
        match_stats_expanded[numeric_cols] = match_stats_expanded[numeric_cols].fillna(0)
    else:
        logger.info(f"   ✅ No missing values in numeric columns")
    
    # Summary statistics
    logger.info(f"\n📊 Final DataFrame Summary:")
    logger.info(f"   Shape: {match_stats_expanded.shape}")
    logger.info(f"   Total records: {len(match_stats_expanded)}")
    logger.info(f"   Total columns: {match_stats_expanded.shape[1]}")
    
    sample_numeric = match_stats_expanded.select_dtypes(include=['number']).head(3)
    logger.info(f"   Sample numeric data shape: {sample_numeric.shape}")
    
    # Save expanded stats
    output_path = Path('data/processed/match_stats_expanded.pkl')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, 'wb') as f:
            pickle.dump(match_stats_expanded, f)
        logger.success(f"✅ Saved expanded match stats to {output_path}")
        logger.success(f"   Columns: {match_stats_expanded.shape[1]}")
        logger.success(f"   Records: {len(match_stats_expanded)}")
    except Exception as e:
        logger.error(f"❌ Error saving to {output_path}: {e}")
        return False
    
    # Save info about columns
    info_path = Path('data/processed/match_stats_columns.pkl')
    try:
        with open(info_path, 'wb') as f:
            pickle.dump({
                'columns': list(match_stats_expanded.columns),
                'dtypes': match_stats_expanded.dtypes.to_dict(),
                'shape': match_stats_expanded.shape
            }, f)
        logger.info(f"   Column info saved to {info_path}")
    except Exception as e:
        logger.warning(f"⚠️  Could not save column info: {e}")
    
    logger.info("\n" + "=" * 80)
    logger.success("SCRIPT 07 COMPLETED SUCCESSFULLY")
    logger.info("=" * 80)
    return True


if __name__ == '__main__':
    success = run_match_stats_expansion()
    sys.exit(0 if success else 1)
