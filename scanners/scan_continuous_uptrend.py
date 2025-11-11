"""
Scan C: Continuous Uptrend Scanner
Identifies stocks with consecutive days of higher closes (default 4+ days)
"""

import pandas as pd
from typing import List, Tuple


def scan_continuous_uptrend(data: pd.DataFrame, min_days: int = 4) -> List[Tuple[str, int, float]]:
    """
    Scan for continuous uptrends (consecutive days with higher closes).
    
    Args:
        data: Stock price data with OHLCV columns
        min_days: Minimum consecutive days (default 4)
    
    Returns:
        List of tuples (end_date, num_days, end_price)
        Each tuple represents the end of an uptrend sequence
    
    Example:
        >>> data = yf.download('NVDA', period='1mo')
        >>> results = scan_continuous_uptrend(data, min_days=4)
        >>> for date, days, price in results:
        ...     print(f"{date}: {days} days uptrend, ended at ${price:.2f}")
    """
    results = []
    
    if len(data) < min_days:
        return results
    
    consecutive_days = 1
    
    for idx in range(1, len(data)):
        if data['Close'].iloc[idx] > data['Close'].iloc[idx - 1]:
            consecutive_days += 1
            
            if consecutive_days >= min_days:
                date = data.index[idx].strftime('%Y-%m-%d')
                close_price = data['Close'].iloc[idx]
                results.append((date, consecutive_days, close_price))
        else:
            consecutive_days = 1
    
    return results


def format_results(results: List[Tuple[str, int, float]], ticker: str) -> List[dict]:
    """
    Format scan results into a dictionary structure for display.
    
    Args:
        results: List of tuples from scan_continuous_uptrend()
        ticker: Stock ticker symbol
    
    Returns:
        List of dictionaries with formatted data
    """
    formatted = []
    
    for date, num_days, close_price in results:
        formatted.append({
            'Ticker': ticker,
            'End Date': date,
            'Consecutive Days': num_days,
            'Close Price': f"${close_price:.2f}"
        })
    
    return formatted


def get_description() -> str:
    """
    Get a description of this scanning criterion.
    
    Returns:
        String description of the scan
    """
    return "Identifies stocks with 4 or more consecutive days of higher closes"


def get_name() -> str:
    """
    Get the name of this scanning criterion.
    
    Returns:
        String name of the scan
    """
    return "Continuous Uptrend (≥4 days)"
