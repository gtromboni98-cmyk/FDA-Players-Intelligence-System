"""
Script 09: PCA Score Calculation
Calculates 13 PCA-based performance scores per match and per player.
Input:  data/processed/match_stats_with_positions.pkl (from script 08)
Output: data/processed/match_stats_with_pca_scores.pkl
        data/processed/player_pca_rankings.pkl
"""

import sys
import pickle
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.features.pca_scoring import (
    calculate_all_pca_scores,
    aggregate_player_scores,
    score_distribution_summary,
    get_pca_score_names
)
from src.config import MIN_MATCHES_PLAYED
from src.utils import Logger

logger = Logger(__name__)


def run_pca_score_calculation():
    """
    Main execution function.
    1. Load match stats with positions
    2. Calculate all 13 PCA scores at match level
    3. Aggregate to player level
    4. Generate rankings and summaries
    5. Save results
    """
    
    logger.info("=" * 80)
    logger.info("SCRIPT 09: PCA Score Calculation")
    logger.info("=" * 80)
    logger.info(f"Calculating {len(get_pca_score_names())} PCA scores...")
    logger.info(f"  Scores: {', '.join(get_pca_score_names())[:60]}...")
    
    # Load match stats with positions
    input_path = Path('data/processed/match_stats_with_positions.pkl')
    if not input_path.exists():
        logger.error(f"❌ File not found: {input_path}")
        logger.error("   Please run script 08 first to map positions")
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
    
    logger.info(f"   Input shape: {match_stats.shape}")
    logger.info(f"   Available columns: {len(match_stats.columns)}")
    
    # Calculate all PCA scores
    logger.info(f"\n🎯 Calculating 13 PCA scores...")
    try:
        match_stats_with_scores = calculate_all_pca_scores(match_stats, verbose=True)
        logger.success(f"✅ All PCA scores calculated")
        logger.info(f"   Output shape: {match_stats_with_scores.shape}")
    except Exception as e:
        logger.error(f"❌ Error calculating PCA scores: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
    
    # Save match-level scores
    match_output_path = Path('data/processed/match_stats_with_pca_scores.pkl')
    match_output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(match_output_path, 'wb') as f:
            pickle.dump(match_stats_with_scores, f)
        logger.success(f"✅ Saved match-level scores to {match_output_path}")
        logger.info(f"   Records: {len(match_stats_with_scores)}")
        logger.info(f"   Columns: {match_stats_with_scores.shape[1]}")
    except Exception as e:
        logger.error(f"❌ Error saving match scores: {e}")
        return False
    
    # Aggregate to player level
    logger.info(f"\n👤 Aggregating scores to player level...")
    
    # Identify player ID column
    player_id_col = 'playerId'
    if player_id_col not in match_stats_with_scores.columns:
        if 'playerID' in match_stats_with_scores.columns:
            player_id_col = 'playerID'
        elif 'player_id' in match_stats_with_scores.columns:
            player_id_col = 'player_id'
        else:
            logger.error("❌ Could not find player ID column")
            logger.error(f"   Available columns: {list(match_stats_with_scores.columns)[:10]}...")
            return False
    
    try:
        player_scores = aggregate_player_scores(
            match_stats_with_scores, 
            player_id_col=player_id_col,
            verbose=True
        )
        logger.success(f"✅ Aggregated to {len(player_scores)} unique players")
    except Exception as e:
        logger.error(f"❌ Error aggregating player scores: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
    
    # Filter by minimum matches
    logger.info(f"\n🔍 Filtering by minimum matches ({MIN_MATCHES_PLAYED})...")
    initial_count = len(player_scores)
    player_scores = player_scores[player_scores['matches_counted'] >= MIN_MATCHES_PLAYED]
    filtered_count = initial_count - len(player_scores)
    logger.info(f"   Removed {filtered_count} players with < {MIN_MATCHES_PLAYED} matches")
    logger.success(f"✅ {len(player_scores)} players remain after filtering")
    
    # Save player rankings
    player_output_path = Path('data/processed/player_pca_rankings.pkl')
    try:
        with open(player_output_path, 'wb') as f:
            pickle.dump(player_scores, f)
        logger.success(f"✅ Saved player rankings to {player_output_path}")
    except Exception as e:
        logger.error(f"❌ Error saving player rankings: {e}")
        return False
    
    # Score distribution summary
    logger.info(f"\n📊 Score Distribution Summary:")
    try:
        distribution = score_distribution_summary(match_stats_with_scores, verbose=True)
    except Exception as e:
        logger.warning(f"⚠️  Could not generate distribution summary: {e}")
    
    # Additional statistics
    logger.info(f"\n📋 Additional Statistics:")
    for score_name in get_pca_score_names()[:3]:
        if score_name in player_scores.columns:
            mean_col = f'{score_name}_mean'
            if mean_col in player_scores.columns:
                values = player_scores[mean_col].dropna()
                logger.info(f"   {score_name}:")
                logger.info(f"     Top player mean: {values.max():.3f}")
                logger.info(f"     Top 10 avg: {values.nlargest(10).mean():.3f}")
    
    logger.info("\n" + "=" * 80)
    logger.success("SCRIPT 09 COMPLETED SUCCESSFULLY")
    logger.success(f"Generated PCA scores for {len(match_stats_with_scores)} matches")
    logger.success(f"Ranked {len(player_scores)} players")
    logger.info("=" * 80)
    return True


if __name__ == '__main__':
    success = run_pca_score_calculation()
    sys.exit(0 if success else 1)
