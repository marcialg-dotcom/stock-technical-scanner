"""
Stock Scanner Library Package

This package contains four independent scanning modules:
- scan_price_surge: Scan A - Price Surge (>5%)
- scan_upward_gap: Scan B - Upward Gap
- scan_continuous_uptrend: Scan C - Continuous Uptrend (≥4 days)
- scan_volume_breakout: Scan D - Volume Breakout

Each module can be imported and used independently.
"""

from .scan_price_surge import scan_price_surge
from .scan_upward_gap import scan_upward_gap
from .scan_continuous_uptrend import scan_continuous_uptrend
from .scan_volume_breakout import scan_volume_breakout

__all__ = [
    'scan_price_surge',
    'scan_upward_gap',
    'scan_continuous_uptrend',
    'scan_volume_breakout'
]

__version__ = '1.0.0'
__author__ = 'Stock Scanner Team'
