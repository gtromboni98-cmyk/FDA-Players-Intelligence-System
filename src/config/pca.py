"""
PCA (Principal Component Analysis) scoring configuration.
Defines the 13 performance dimensions and feature sets for player evaluation.
"""

import os

# ============================================================================
# PCA SCORE DEFINITIONS - Feature sets for each of the 13 scores
# ============================================================================
PCA_SCORE_DEFINITIONS = {
    # Defensive Metrics
    'DEFENSE_SCORE': [
        'duels', 'defensiveDuels', 'aerialDuels', 'looseBallDuels',
        'pressingDuels', 'defensiveActions', 'fouls', 'clearances',
        'slidingTackles', 'shotsBlocked', 'dribblesAgainst'
    ],
    'DEFENSE_EFFICIENCY': [
        'duelsWon_percent', 'defensiveDuelsWon_percent', 'aerialDuelsWon_percent',
        'dribblesAgainstWon_percent', 'pressingDuelsWon', 'looseBallDuelsWon',
        'successfulSlidingTackles_percent'
    ],
    'BALL_RECOVERY': [
        'interceptions', 'ballRecoveries', 'opponentHalfRecoveries',
        'dangerousOpponentHalfRecoveries', 'counterpressingRecoveries'
    ],
    'BALL_LOSSES': [
        'losses', 'ownHalfLosses', 'ballLosses',
        'missedBalls', 'dangerousOwnHalfLosses'
    ],
    
    # Playmaking Metrics
    'PLAYMAKING': [
        'passes', 'forwardPasses', 'backPasses', 'verticalPasses',
        'longPasses', 'passesToFinalThird', 'crosses', 'lateralPasses',
        'corners', 'receivedPass'
    ],
    'PASSING_EFFICIENCY': [
        'successfulPasses_percent', 'successfulForwardPasses_percent',
        'successfulBackPasses_percent', 'successfulVerticalPasses_percent',
        'successfulLongPasses_percent', 'successfulPassesToFinalThird_percent',
        'successfulCrosses_percent', 'successfulLateralPasses_percent'
    ],
    'PASSING_STYLE': [
        'passLength', 'longPassLength'
    ],
    
    # Progression Metrics
    'PROGRESSION': [
        'dribbles', 'accelerations', 'progressivePasses', 'passesToFinalThird',
        'offensiveDuels', 'dribbleDistanceFromOpponentGoal', 'progressiveRun'
    ],
    'PROGRESSION_EFFICIENCY': [
        'successfulDribbles_percent', 'successfulProgressivePasses_percent',
        'successfulPassesToFinalThird_percent', 'offensiveDuelsWon_percent'
    ],
    
    # Attacking Metrics
    'FORWARD_ACTIVITY': [
        'shots', 'shotsOnTarget_percent', 'headShots', 'attackingActions',
        'xgShot', 'touchInBox', 'offsides', 'linkupPlays', 'penalties'
    ],
    'SHOOTING_EFFICIENCY': [
        'headShotsOnTarget_percent', 'goalConversion_percent',
        'directFreeKicksOnTarget_percent', 'goals', 'successfulLinkupPlays_percent'
    ],
    
    # Creating & Assisting
    'CHANCE_CREATION': [
        'assists', 'keyPasses', 'shotAssists', 'smartPasses',
        'throughPasses', 'shotOnTargetAssists', 'xgAssist',
        'secondAssists', 'thirdAssists'
    ],
    'CHANCE_EFFICIENCY': [
        'successfulSmartPasses_percent', 'successfulKeyPasses_percent',
        'successfulShotAssists_percent', 'assists', 'successfulThroughPasses_percent'
    ]
}

# ============================================================================
# PCA & FILTERING PARAMETERS
# ============================================================================
PCA_N_COMPONENTS = 1  # Always use 1 component to get a single score per dimension

MIN_MINUTES_PLAYED = int(os.getenv("MIN_MINUTES_PLAYED", "3000"))
# ~30 matches @ 100 min/match, or ~15 matches @ 200 min/match
# Ensures statistically significant data

MIN_MATCHES_PLAYED = int(os.getenv("MIN_MATCHES_PLAYED", "5"))
# Minimum matches with >= 10 minutes
# Prevents single-outlier matches from skewing player rankings
