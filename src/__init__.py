"""
FDA Players Intelligence System - Main Package
"""

from . import ingestion
from . import features
from . import models

__version__ = "0.1.0"
__all__ = ['ingestion', 'features', 'models']
