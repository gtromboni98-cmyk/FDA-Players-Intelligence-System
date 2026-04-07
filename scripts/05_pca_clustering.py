"""
FASE 5: PCA & Clustering Analysis
Riduce dimensionalità con PCA e cluster con K-Means.
"""

from src.utils import Logger, DataManager
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pickle

Logger.print_section("FASE 5: PCA & Clustering Analysis")

manager = DataManager()

# Load clean player stats
df_players = manager.load_pickle('data/processed/players_stats_clean.pkl')

Logger.print_info(f"Input shape: {df_players.shape}")

# Select numeric features
numeric_cols = df_players.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols = [col for col in numeric_cols if col != 'player_wyId']

X = df_players[numeric_cols].fillna(0)

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

Logger.print_info(f"Features: {len(numeric_cols)}")

# PCA - 95% variance
pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X_scaled)

Logger.print_success(f"PCA: {X_pca.shape[1]} components explain 95% variance")

# K-Means clustering (7 clusters)
kmeans = KMeans(n_clusters=7, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_pca)

Logger.print_info(f"Clustering distribution:")
for cluster_id in range(7):
    count = (clusters == cluster_id).sum()
    Logger.print_info(f"  Cluster {cluster_id}: {count} players")

# Save results
df_pca_results = df_players[['player_wyId', 'player_name']].copy()
df_pca_results['cluster'] = clusters
for i in range(min(3, X_pca.shape[1])):  # Save top 3 PCA components
    df_pca_results[f'PC{i+1}'] = X_pca[:, i]

manager.save_pickle({
    'pca_results': df_pca_results,
    'pca_model': pca,
    'kmeans_model': kmeans,
    'scaler': scaler
}, 'data/processed/pca_clustering_models.pkl')

manager.save_dataframe(df_pca_results, 'data/processed/pca_clusters.csv')

Logger.print_success("PCA & Clustering models saved")
