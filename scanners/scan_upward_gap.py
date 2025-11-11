"""
Scan B: Upward Gap Scanner
Identifies stocks that opened more than a threshold above previous close (default 1%)
"""

import pandas as pd
from typing import List, Tuple


def scan_upward_gap(data: pd.DataFrame, threshold: float = 0.01) -> List[Tuple[str, float, float]]:
    """
    Scan for upward gaps where open > previous close * (1 + threshold).
    
    Args:
        data: Stock price data with OHLCV columns
        threshold: Gap threshold (default 0.01 = 1%)
    
    Returns:
        List of tuples (date, gap_pct, open_price)
        Each tuple represents a day with an upward gap
    
    Example:
        >>> data = yf.download('TSLA', period='1mo')
        >>> results = scan_upward_gap(data, threshold=0.01)
        >>> for date, gap_pct, price in results:
        ...     print(f"{date}: Gap up {gap_pct:.2f}% at ${price:.2f}")
    """
    results = []
    
    if len(data) < 2:
        return results
    
    for idx in range(1, len(data)):
        prev_close = data['Close'].iloc[idx - 1]
        curr_open = data['Open'].iloc[idx]
        
        if curr_open > prev_close * (1 + threshold):
            date = data.index[idx].strftime('%Y-%m-%d')
            gap_pct = ((curr_open - prev_close) / prev_close) * 100
            results.append((date, gap_pct, curr_open))
    
    return results


def format_results(results: List[Tuple[str, float, float]], ticker: str) -> List[dict]:
    """
    Format scan results into a dictionary structure for display.
    
    Args:
        results: List of tuples from scan_upward_gap()
        ticker: Stock ticker symbol
    
    Returns:
        List of dictionaries with formatted data
    """
    formatted = []
    
    for date, gap_pct, open_price in results:
        formatted.append({
            'Ticker': ticker,
            'Date': date,
            'Gap (%)': f"{gap_pct:.2f}",
            'Open Price': f"${open_price:.2f}"
        })
    
    return formatted


def get_description() -> str:
    """
    Get a description of this scanning criterion.
    
    Returns:
        String description of the scan
    """
    return "Identifies stocks that opened more than 1% above previous close"


def get_name() -> str:
    """
    Get the name of this scanning criterion.
    
    Returns:
        String name of the scan
    """
    return "Upward Gap"
