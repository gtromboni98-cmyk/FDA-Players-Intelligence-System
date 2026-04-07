"""
Script 08: Position Mapping
Maps detailed player positions to 9 generalized roles.
Input:  data/processed/match_stats_expanded.pkl (from script 07)
Output: data/processed/match_stats_with_positions.pkl
"""

import sys
import pickle
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.features.position_mapping import (
    apply_position_mapping,
    get_available_positions,
    get_position_distribution,
    filter_by_position
)
from src.utils import Logger

logger = Logger(__name__)


def run_position_mapping():
    """
    Main execution function.
    1. Load expanded match stats
    2. Map positions from detailed to 9 generalized roles
    3. Create position-specific DataFrames
    4. Save results
    """
    
    logger.info("=" * 80)
    logger.info("SCRIPT 08: Position Mapping")
    logger.info("=" * 80)
    
    # Load expanded match stats
    input_path = Path('data/processed/match_stats_expanded.pkl')
    if not input_path.exists():
        logger.error(f"❌ File not found: {input_path}")
        logger.error("   Please run script 07 first to expand match statistics")
        return False
    
    try:
        with open(input_path, 'rb') as f:
            match_stats = pickle.load(f)
        logger.info(f"✅ Loaded {len(match_stats)} match records from {input_path}")
    except Exception as e:
        logger.error(f"❌ Error loading {input_path}: {e}")
        return False
    
    # Convert to DataFrame if needed
    if not isinstance(match_stats, pd.DataFrame):
        match_stats = pd.DataFrame(match_stats)
    
    # Check for position column
    if 'position' not in match_stats.columns:
        logger.warning("⚠️  'position' column not found in DataFrame")
        logger.warning("   Attempting to infer from other columns...")
        if 'Role' in match_stats.columns:
            match_stats['position'] = match_stats['Role']
        else:
            logger.error("❌ No position information found")
            return False
    
    logger.info(f"   Input shape: {match_stats.shape}")
    initial_positions = match_stats['position'].unique()
    logger.info(f"   Unique input positions: {len(initial_positions)}")
    
    # Apply position mapping
    logger.info("\n🗺️  Mapping positions to 9 generalized roles...")
    try:
        match_stats = apply_position_mapping(match_stats, position_column='position')
        logger.success(f"✅ Position mapping applied")
    except Exception as e:
        logger.error(f"❌ Error applying position mapping: {e}")
        return False
    
    # Show distribution
    logger.info("\n📊 Position Distribution After Mapping:")
    try:
        dist = get_position_distribution(match_stats)
        for position, count in sorted(dist.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(match_stats)) * 100
            bar = "█" * int(pct / 2)
            logger.info(f"   {position:20s} {count:6d} ({pct:5.1f}%) {bar}")
    except Exception as e:
        logger.warning(f"⚠️  Could not display distribution: {e}")
    
    # Get available positions
    available_positions = get_available_positions()
    logger.info(f"\n   ✅ Available generalized positions: {', '.join(available_positions)}")
    
    # Save main DataFrame with positions
    output_path = Path('data/processed/match_stats_with_positions.pkl')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, 'wb') as f:
            pickle.dump(match_stats, f)
        logger.success(f"✅ Saved match stats with positions to {output_path}")
    except Exception as e:
        logger.error(f"❌ Error saving to {output_path}: {e}")
        return False
    
    # Create and save position-specific DataFrames
    logger.info(f"\n📁 Creating position-specific DataFrames...")
    position_files = {}
    
    for position in available_positions:
        try:
            pos_df = filter_by_position(match_stats, position)
            if len(pos_df) > 0:
                pos_file = Path('data/processed') / f'match_stats_{position.lower().replace(" ", "_")}.pkl'
                with open(pos_file, 'wb') as f:
                    pickle.dump(pos_df, f)
                position_files[position] = pos_file
                logger.info(f"   ✅ {position:20s} {len(pos_df):6d} records → {pos_file.name}")
        except Exception as e:
            logger.warning(f"   ⚠️  Could not create {position}: {e}")
    
    # Summary
    logger.info(f"\n📋 Summary:")
    logger.info(f"   Total records: {len(match_stats)}")
    logger.info(f"   Positions mapped: {len(position_files)}")
    logger.info(f"   Output files created: {len(position_files)}")
    
    logger.info("\n" + "=" * 80)
    logger.success("SCRIPT 08 COMPLETED SUCCESSFULLY")
    logger.info("=" * 80)
    return True


if __name__ == '__main__':
    success = run_position_mapping()
    sys.exit(0 if success else 1)
