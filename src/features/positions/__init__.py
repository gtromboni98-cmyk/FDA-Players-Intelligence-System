"""
Position mapping and categorization module.
"""

from .mapping import (
    generalize_position,
    generalize_position_from_list,
    apply_position_mapping,
    get_available_positions,
    filter_by_position,
    get_position_distribution
)

__all__ = [
    'generalize_position',
    'generalize_position_from_list',
    'apply_position_mapping',
    'get_available_positions',
    'filter_by_position',
    'get_position_distribution'
]
