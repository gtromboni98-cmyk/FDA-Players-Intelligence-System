"""
PIPELINE COMPLETA - Esegui tutte le fasi in sequenza
Dalla ingestion ai ranking finali.
"""

from src.utils import Logger
import subprocess
import sys

stages = [
    ('01_fetch_data.py', 'Data Ingestion'),
    ('02_player_profiling.py', 'Player Profiling'),
    ('03_fetch_advanced_stats.py', 'Advanced Stats'),
    ('04_data_cleaning.py', 'Data Cleaning'),
    ('05_pca_clustering.py', 'PCA & Clustering'),
    ('06_position_scoring.py', 'Position Scoring'),
]

Logger.print_section("FDA PLAYERS INTELLIGENCE - COMPLETE PIPELINE")

for script, stage_name in stages:
    Logger.print_section(f"RUNNING: {stage_name}")
    
    result = subprocess.run(
        [sys.executable, f'scripts/{script}'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        Logger.print_success(f"{stage_name} completed ✓")
    else:
        Logger.print_error(f"{stage_name} failed ✗")
        print(result.stderr)
        break

Logger.print_section("PIPELINE COMPLETE")
Logger.print_success("All stages completed successfully!")
Logger.print_info("Results saved in data/processed/")
