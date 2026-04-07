"""
Script 10: Player Intelligence Profiling & Final Ranking
Generates final player profiles, rankings, and intelligence summaries.
Input:  data/processed/match_stats_with_pca_scores.pkl (from script 09)
        data/processed/player_pca_rankings.pkl
Output: data/processed/player_intelligence_profiles.pkl
        data/rankings/final_player_rankings.pkl
"""

import sys
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.features.pca_scoring import get_pca_score_names
from src.config import MIN_MATCHES_PLAYED
from src.utils import Logger

logger = Logger(__name__)


def calculate_overall_rating(player_row: pd.Series, weights: Optional[Dict[str, float]] = None) -> float:
    """
    Calculates overall player rating from individual PCA scores.
    
    Default weighted approach:
    - Defensive: 25%
    - Playmaking: 25%
    - Progression: 25%
    - Attacking: 25%
    """
    
    if weights is None:
        weights = {
            'defensive': ['DEFENSE_SCORE', 'DEFENSE_EFFICIENCY', 'BALL_RECOVERY'],
            'playmaking': ['PLAYMAKING', 'PASSING_EFFICIENCY', 'PASSING_STYLE'],
            'progression': ['PROGRESSION', 'PROGRESSION_EFFICIENCY'],
            'attacking': ['FORWARD_ACTIVITY', 'SHOOTING_EFFICIENCY', 'CHANCE_CREATION', 'CHANCE_EFFICIENCY']
        }
    
    category_scores = {}
    
    for category, scores in weights.items():
        score_values = []
        for score_name in scores:
            mean_col = f'{score_name}_mean'
            if mean_col in player_row.index:
                val = player_row[mean_col]
                if pd.notna(val):
                    score_values.append(val)
        
        if score_values:
            category_scores[category] = np.mean(score_values)
    
    if category_scores:
        return np.mean(list(category_scores.values()))
    else:
        return 0.0


def get_player_strengths(player_row: pd.Series, top_n: int = 3) -> List[str]:
    """
    Identifies top N score dimensions for a player.
    """
    score_names = get_pca_score_names()
    scores_dict = {}
    
    for score_name in score_names:
        mean_col = f'{score_name}_mean'
        if mean_col in player_row.index:
            val = player_row[mean_col]
            if pd.notna(val):
                scores_dict[score_name] = val
    
    if not scores_dict:
        return []
    
    sorted_scores = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
    return [name for name, _ in sorted_scores[:top_n]]


def get_player_weaknesses(player_row: pd.Series, top_n: int = 3) -> List[str]:
    """
    Identifies bottom N score dimensions for a player.
    """
    score_names = get_pca_score_names()
    scores_dict = {}
    
    for score_name in score_names:
        mean_col = f'{score_name}_mean'
        if mean_col in player_row.index:
            val = player_row[mean_col]
            if pd.notna(val):
                scores_dict[score_name] = val
    
    if not scores_dict:
        return []
    
    sorted_scores = sorted(scores_dict.items(), key=lambda x: x[1])
    return [name for name, _ in sorted_scores[:top_n]]


def create_player_profiles(player_ranks: pd.DataFrame, 
                           match_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Creates comprehensive player intelligence profiles.
    
    Adds to each player:
    - Overall rating (0-1)
    - Top 3 strengths
    - Top 3 weaknesses
    - Performance consistency (std across matches)
    - Career trajectory info
    """
    
    profiles = player_ranks.copy()
    
    # Calculate overall ratings
    logger.info("   Calculating overall ratings...")
    profiles['overall_rating'] = profiles.apply(
        lambda row: calculate_overall_rating(row),
        axis=1
    )
    
    # Identify strengths
    logger.info("   Identifying player strengths...")
    profiles['strengths'] = profiles.apply(
        lambda row: get_player_strengths(row, top_n=3),
        axis=1
    )
    
    # Identify weaknesses
    logger.info("   Identifying player weaknesses...")
    profiles['weaknesses'] = profiles.apply(
        lambda row: get_player_weaknesses(row, top_n=3),
        axis=1
    )
    
    # Calculate consistency metrics
    logger.info("   Calculating performance consistency...")
    score_names = get_pca_score_names()
    profiles['consistency_score'] = 0.0
    
    consistency_stds = []
    for score_name in score_names:
        std_col = f'{score_name}_std'
        if std_col in profiles.columns:
            consistency_stds.append(profiles[std_col])
    
    if consistency_stds:
        profiles['consistency_score'] = pd.concat(consistency_stds, axis=1).mean(axis=1)
    
    # Get match statistics from match_scores
    logger.info("   Aggregating match statistics...")
    player_id_col = None
    for col in ['playerId', 'playerID', 'player_id']:
        if col in match_scores.columns and col in profiles.columns:
            player_id_col = col
            break
    
    if player_id_col:
        match_stats = match_scores.groupby(player_id_col).agg({
            'minutesOnField': 'sum',
            'goals': 'sum',
            'assists': 'sum',
            'yellowCards': 'sum',
            'redCards': 'sum'
        }).reset_index()
        
        # Merge into profiles
        profiles = profiles.merge(match_stats, on=player_id_col, how='left', suffixes=('', '_total'))
    
    return profiles


def create_final_rankings(player_profiles: pd.DataFrame) -> pd.DataFrame:
    """
    Creates final rankings sorted by overall rating.
    Adds rank, percentile, and tier classifications.
    """
    
    rankings = player_profiles.copy()
    rankings['rank'] = rankings['overall_rating'].rank(method='dense', ascending=False).astype(int)
    rankings['percentile'] = rankings['overall_rating'].rank(pct=True) * 100
    
    # Classification tiers
    def classify_tier(rating):
        if pd.isna(rating):
            return 'Unrated'
        elif rating >= 0.8:
            return 'Elite'
        elif rating >= 0.6:
            return 'Top Professional'
        elif rating >= 0.4:
            return 'Professional'
        else:
            return 'Developing'
    
    rankings['tier'] = rankings['overall_rating'].apply(classify_tier)
    
    # Sort by rating
    rankings = rankings.sort_values('overall_rating', ascending=False).reset_index(drop=True)
    
    return rankings


def run_player_profiling():
    """
    Main execution function.
    1. Load player PCA rankings
    2. Load match-level scores
    3. Create player profiles with strengths/weaknesses
    4. Generate final rankings
    5. Save results
    """
    
    logger.info("=" * 80)
    logger.info("SCRIPT 10: Player Intelligence Profiling & Final Ranking")
    logger.info("=" * 80)
    
    # Load player rankings from script 09
    player_path = Path('data/processed/player_pca_rankings.pkl')
    if not player_path.exists():
        logger.error(f"❌ File not found: {player_path}")
        logger.error("   Please run script 09 first to calculate PCA scores")
        return False
    
    try:
        with open(player_path, 'rb') as f:
            player_ranks = pickle.load(f)
        logger.info(f"✅ Loaded {len(player_ranks)} player rankings from {player_path}")
    except Exception as e:
        logger.error(f"❌ Error loading {player_path}: {e}")
        return False
    
    if not isinstance(player_ranks, pd.DataFrame):
        player_ranks = pd.DataFrame(player_ranks)
    
    # Load match-level scores
    match_path = Path('data/processed/match_stats_with_pca_scores.pkl')
    match_scores = None
    
    if match_path.exists():
        try:
            with open(match_path, 'rb') as f:
                match_scores = pickle.load(f)
            logger.info(f"✅ Loaded {len(match_scores)} match scores from {match_path}")
        except Exception as e:
            logger.warning(f"⚠️  Could not load match scores: {e}")
    
    # Create profiles
    logger.info(f"\n👤 Creating player intelligence profiles...")
    if match_scores is not None and isinstance(match_scores, pd.DataFrame):
        try:
            player_profiles = create_player_profiles(player_ranks, match_scores)
            logger.success(f"✅ Created profiles for {len(player_profiles)} players")
        except Exception as e:
            logger.warning(f"⚠️  Error creating profiles: {e}")
            player_profiles = player_ranks
    else:
        logger.warning("⚠️  Match scores not available, using ranking data only")
        player_profiles = player_ranks
    
    # Create final rankings
    logger.info(f"\n🏆 Creating final rankings...")
    try:
        final_rankings = create_final_rankings(player_profiles)
        logger.success(f"✅ Created rankings for {len(final_rankings)} players")
    except Exception as e:
        logger.error(f"❌ Error creating rankings: {e}")
        return False
    
    # Display top players
    logger.info(f"\n🌟 Top 10 Players:")
    top_10 = final_rankings.head(10)
    for idx, row in top_10.iterrows():
        player_id = row.iloc[0]  # First column
        rating = row.get('overall_rating', 0)
        tier = row.get('tier', 'Unknown')
        matches = row.get('matches_counted', 0)
        logger.info(f"   #{row.get('rank', idx+1)}: Player {player_id} | Rating: {rating:.3f} | Tier: {tier} | Matches: {int(matches)}")
    
    # Distribution by tier
    if 'tier' in final_rankings.columns:
        logger.info(f"\n📊 Player Distribution by Tier:")
        tier_counts = final_rankings['tier'].value_counts()
        for tier, count in tier_counts.items():
            pct = (count / len(final_rankings)) * 100
            logger.info(f"   {tier:20s} {count:6d} ({pct:5.1f}%)")
    
    # Save player profiles
    profiles_path = Path('data/processed/player_intelligence_profiles.pkl')
    profiles_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(profiles_path, 'wb') as f:
            pickle.dump(player_profiles, f)
        logger.success(f"✅ Saved player intelligence profiles to {profiles_path}")
    except Exception as e:
        logger.error(f"❌ Error saving profiles: {e}")
        return False
    
    # Save final rankings
    rankings_path = Path('data/rankings/final_player_rankings.pkl')
    rankings_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(rankings_path, 'wb') as f:
            pickle.dump(final_rankings, f)
        logger.success(f"✅ Saved final rankings to {rankings_path}")
        logger.info(f"   Total players: {len(final_rankings)}")
        logger.info(f"   Columns: {len(final_rankings.columns)}")
    except Exception as e:
        logger.error(f"❌ Error saving rankings: {e}")
        return False
    
    # Summary statistics
    logger.info(f"\n📋 Summary Statistics:")
    if 'overall_rating' in final_rankings.columns:
        ratings = final_rankings['overall_rating'].dropna()
        logger.info(f"   Overall Rating - Mean: {ratings.mean():.3f}, Std: {ratings.std():.3f}")
        logger.info(f"   Range: {ratings.min():.3f} - {ratings.max():.3f}")
    
    if 'matches_counted' in final_rankings.columns:
        matches = final_rankings['matches_counted'].dropna()
        logger.info(f"   Matches - Mean: {matches.mean():.1f}, Min: {matches.min():.0f}, Max: {matches.max():.0f}")
    
    logger.info("\n" + "=" * 80)
    logger.success("SCRIPT 10 COMPLETED SUCCESSFULLY")
    logger.success(f"Final intelligence system ready with {len(final_rankings)} player profiles")
    logger.info("=" * 80)
    return True


if __name__ == '__main__':
    success = run_player_profiling()
    sys.exit(0 if success else 1)
