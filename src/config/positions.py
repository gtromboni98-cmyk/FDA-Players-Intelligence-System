"""
Position mapping configuration.
Maps detailed Wyscout positions to 9 generalized player roles.
"""

# ============================================================================
# POSITION MAPPING - Detailed positions to generalized roles
# ============================================================================
POSITION_MAPPING = {
    # Goalkeepers
    'Goalkeeper': 'Goalkeeper',
    
    # Fullbacks
    'Left Back (5 at the back)': 'FullBack',
    'Left Back': 'FullBack',
    'Right Back': 'FullBack',
    'Right Back (5 at the back)': 'FullBack',
    
    # Centre Backs
    'Centre Back': 'CentreBack',
    'Left Centre Back': 'CentreBack',
    'Left Centre Back (3 at the back)': 'CentreBack',
    'Right Centre Back': 'CentreBack',
    'Right Centre Back (3 at the back)': 'CentreBack',
    
    # Defensive Midfielders
    'Defensive Midfielder': 'DefensiveMidfielder',
    'Left Defensive Midfielder': 'DefensiveMidfielder',
    'Right Defensive Midfielder': 'DefensiveMidfielder',
    
    # Centre Midfielders
    'Left Centre Midfielder': 'Midfielder',
    'Right Centre Midfielder': 'Midfielder',
    
    # Attacking Midfielders
    'Attacking Midfielder': 'AttackingMidfielder',
    'Left Attacking Midfielder': 'AttackingMidfielder',
    'Right Attacking Midfielder': 'AttackingMidfielder',
    
    # Wide Midfielders / Wingbacks
    'Left Wingback': 'WideMidfielder',
    'Right Wingback': 'WideMidfielder',
    
    # Wingers
    'Left Winger': 'Winger',
    'Left Wing Forward': 'Winger',
    'Right Winger': 'Winger',
    'Right Wing Forward': 'Winger',
    
    # Strikers
    'Striker': 'Striker'
}

# Generalized position roles (derived from mapping)
GENERALIZED_POSITIONS = sorted(set(POSITION_MAPPING.values()))
