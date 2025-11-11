"""
Scan A: Price Surge Scanner
Identifies stocks with single-day price increases exceeding a threshold (default 5%)
"""

import pandas as pd
from typing import List, Tuple


def scan_price_surge(data: pd.DataFrame, threshold: float = 0.05) -> List[Tuple[str, float, float]]:
    """
    Scan for single-day price surges exceeding threshold.
    
    Args:
        data: Stock price data with OHLCV columns
        threshold: Minimum price change threshold (default 0.05 = 5%)
    
    Returns:
        List of tuples (date, pct_change, close_price)
        Each tuple represents a day where price increased > threshold
    
    Example:
        >>> data = yf.download('AAPL', period='1mo')
        >>> results = scan_price_surge(data, threshold=0.05)
        >>> for date, pct_change, price in results:
        ...     print(f"{date}: +{pct_change:.2f}% at ${price:.2f}")
    """
    results = []
    
    if len(data) < 2:
        return results
    
    # Calculate daily percentage change
    data['PctChange'] = data['Close'].pct_change() * 100
    
    # Find days where change exceeds threshold
    for idx in range(1, len(data)):
        pct_change = data['PctChange'].iloc[idx]
        
        if pct_change > (threshold * 100):
            date = data.index[idx].strftime('%Y-%m-%d')
            close_price = data['Close'].iloc[idx]
            results.append((date, pct_change, close_price))
    
    return results


def format_results(results: List[Tuple[str, float, float]], ticker: str) -> List[dict]:
    """
    Format scan results into a dictionary structure for display.
    
    Args:
        results: List of tuples from scan_price_surge()
        ticker: Stock ticker symbol
    
    Returns:
        List of dictionaries with formatted data
    """
    formatted = []
    
    for date, pct_change, price in results:
        formatted.append({
            'Ticker': ticker,
            'Date': date,
            'Price Change (%)': f"{pct_change:.2f}",
            'Close Price': f"${price:.2f}"
        })
    
    return formatted


def get_description() -> str:
    """
    Get a description of this scanning criterion.
    
    Returns:
        String description of the scan
    """
    return "Identifies stocks with single-day price increases exceeding 5%"


def get_name() -> str:
    """
    Get the name of this scanning criterion.
    
    Returns:
        String name of the scan
    """
    return "Price Surge (>5%)"
