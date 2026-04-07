"""
FASE 4: Data Cleaning & Feature Engineering
Pulisce dati, rimuove rumore, espande feature nested.
"""

from src.features import DataProcessor
from src.utils import Logger, DataManager
import pandas as pd
import numpy as np

Logger.print_section("FASE 4: Data Cleaning & Feature Engineering")

manager = DataManager()
processor = DataProcessor()

# Load raw match stats
df_stats = manager.load_pickle('data/processed/match_stats.pkl')

Logger.print_info(f"Starting shape: {df_stats.shape}")

# Remove goalkeepers (if role info available)
if 'role' in df_stats.columns:
    df_stats = df_stats[df_stats['role'] != 'Goalkeeper']
    Logger.print_info(f"After removing GKs: {df_stats.shape}")
elif 'player_wyId' in df_stats.columns:
    Logger.print_info("No role column - skipping goalkeeper filter")

# Remove players with < 5 matches
player_counts = df_stats.groupby('player_wyId').size()
valid_players = player_counts[player_counts >= 5].index
df_stats = df_stats[df_stats['player_wyId'].isin(valid_players)]
Logger.print_info(f"After filtering <5 matches: {df_stats.shape}")

# Drop high NaN columns (>40%)
null_pct = df_stats.isnull().sum() / len(df_stats)
cols_to_drop = null_pct[null_pct > 0.4].index
df_stats = df_stats.drop(columns=cols_to_drop)
Logger.print_info(f"Dropped {len(cols_to_drop)} high-NaN columns")

# Drop low-variance & high-correlation features
numeric_cols = df_stats.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    if df_stats[col].var() < 0.01:
        df_stats = df_stats.drop(columns=[col])

# Aggregate to player level (mean stats per player)
df_clean = df_stats.groupby('player_wyId').agg({
    'player_name': 'first',
    **{col: 'mean' for col in numeric_cols if col in df_stats.columns}
}).reset_index()

Logger.print_success(f"Final clean shape: {df_clean.shape}")

# Save cleaned data
manager.save_pickle(df_clean, 'data/processed/players_stats_clean.pkl')
manager.save_dataframe(df_clean, 'data/processed/players_stats_clean.csv')

Logger.print_success("Cleaned data saved")
