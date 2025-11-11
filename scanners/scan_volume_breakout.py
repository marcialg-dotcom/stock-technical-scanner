"""
Scan D: Volume Breakout Scanner
Identifies stocks with volume exceeding threshold above their moving average (default 10% above 50-day MA)
"""

import pandas as pd
from typing import List, Tuple


def scan_volume_breakout(data: pd.DataFrame, threshold: float = 0.10, ma_period: int = 50) -> List[Tuple[str, int, int]]:
    """
    Scan for volume breakouts exceeding threshold above moving average.
    
    Args:
        data: Stock price data with OHLCV columns
        threshold: Volume threshold above MA (default 0.10 = 10%)
        ma_period: Moving average period in days (default 50)
    
    Returns:
        List of tuples (date, volume, avg_volume)
        Each tuple represents a day with volume breakout
    
    Example:
        >>> data = yf.download('GME', period='3mo')
        >>> results = scan_volume_breakout(data, threshold=0.10, ma_period=50)
        >>> for date, vol, avg_vol in results:
        ...     print(f"{date}: Volume {vol:,} vs avg {avg_vol:,}")
    """
    results = []
    
    if len(data) < ma_period:
        return results
    
    # Calculate moving average of volume
    data['VolumeMA'] = data['Volume'].rolling(window=ma_period).mean()
    
    # Find days where volume exceeds threshold above MA
    for idx in range(ma_period, len(data)):
        volume = data['Volume'].iloc[idx]
        avg_volume = data['VolumeMA'].iloc[idx]
        
        if pd.notna(avg_volume) and volume > avg_volume * (1 + threshold):
            date = data.index[idx].strftime('%Y-%m-%d')
            results.append((date, int(volume), int(avg_volume)))
    
    return results


def format_results(results: List[Tuple[str, int, int]], ticker: str) -> List[dict]:
    """
    Format scan results into a dictionary structure for display.
    
    Args:
        results: List of tuples from scan_volume_breakout()
        ticker: Stock ticker symbol
    
    Returns:
        List of dictionaries with formatted data
    """
    formatted = []
    
    for date, volume, avg_volume in results:
        pct_above = ((volume - avg_volume) / avg_volume) * 100
        formatted.append({
            'Ticker': ticker,
            'Date': date,
            'Volume': f"{volume:,}",
            'Avg Volume (50d)': f"{avg_volume:,}",
            'Above Avg (%)': f"{pct_above:.2f}"
        })
    
    return formatted


def get_description() -> str:
    """
    Get a description of this scanning criterion.
    
    Returns:
        String description of the scan
    """
    return "Identifies stocks with volume exceeding 10% above their 50-day average"


def get_name() -> str:
    """
    Get the name of this scanning criterion.
    
    Returns:
        String name of the scan
    """
    return "Volume Breakout"
