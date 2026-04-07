"""
FASE 6: Position-Specific PCA Scoring
Crea 13 score sintetici per ruolo (Defence, Passing, Progression, Shooting, etc).
"""

from src.utils import Logger, DataManager
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

Logger.print_section("FASE 6: Position-Specific Scoring")

manager = DataManager()

# Load clean player stats
df_players = manager.load_pickle('data/processed/players_stats_clean.pkl')

Logger.print_info(f"Scoring {len(df_players)} players...")

# Define score categories (simplified mapping)
SCORE_CATEGORIES = {
    'DEFENSE_SCORE': ['tackles', 'interceptions', 'clearances'],
    'DEFENSE_EFFICIENCY': ['tackle_success_pct', 'interception_success_pct'],
    'BALL_RECOVERY': ['ball_recovery', 'loose_ball_recovery'],
    'PLAYMAKING': ['passes_total', 'pass_forward', 'pass_back'],
    'PASSING_EFFICIENCY': ['pass_accuracy_pct', 'pass_forward_accuracy'],
    'PROGRESSION': ['progressive_passes', 'progressive_runs'],
    'FORWARD_ACTIVITY': ['shots', 'shots_on_target', 'touches_in_box'],
    'SHOOTING_EFFICIENCY': ['shot_accuracy_pct', 'xg'],
    'CHANCE_CREATION': ['assists', 'key_pass', 'chance_created'],
}

# Calculate scores (normalized 0-100)
df_scores = df_players[['player_wyId', 'player_name']].copy()

for score_name, features in SCORE_CATEGORIES.items():
    # Get available features
    available_features = [f for f in features if f in df_players.columns]
    
    if available_features:
        X = df_players[available_features].fillna(0)
        X_scaled = StandardScaler().fit_transform(X)
        
        # Simple aggregation: mean of normalized features, then scale to 0-100
        score_array = X_scaled.mean(axis=1)
        min_val = score_array.min()
        max_val = score_array.max()
        
        if min_val == max_val:
            normalized_score = np.full_like(score_array, 50.0)
        else:
            normalized_score = ((score_array - min_val) / (max_val - min_val)) * 100
        
        df_scores[score_name] = normalized_score

Logger.print_success(f"Calculated {len(SCORE_CATEGORIES)} position scores")

# Rank players by overall score
df_scores['OVERALL_SCORE'] = df_scores[[col for col in df_scores.columns if 'SCORE' in col or 'EFFICIENCY' in col]].mean(axis=1)

top_players = df_scores.nlargest(10, 'OVERALL_SCORE')
Logger.print_info("Top 10 players by overall score:")
for idx, row in top_players.iterrows():
    Logger.print_info(f"  {row['player_name']}: {row['OVERALL_SCORE']:.1f}")

# Save scores
manager.save_dataframe(df_scores, 'data/processed/player_position_scores.csv')
manager.save_pickle(df_scores, 'data/processed/player_position_scores.pkl')

Logger.print_success("Position scores saved")
