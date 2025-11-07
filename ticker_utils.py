"""
Utility functions for fetching stock ticker lists from various exchanges.
"""
import pandas as pd
import urllib.request
from typing import List


def get_nasdaq_tickers() -> List[str]:
    """Fetch NASDAQ ticker symbols."""
    try:
        url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        # For simplicity, we'll use a predefined list of major NASDAQ stocks
        # In production, you'd want to use a proper API or data source
        nasdaq_tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'AVGO', 'COST',
            'NFLX', 'AMD', 'PEP', 'ADBE', 'CSCO', 'CMCSA', 'INTC', 'TXN', 'QCOM', 'INTU',
            'AMGN', 'AMAT', 'HON', 'SBUX', 'ISRG', 'BKNG', 'MDLZ', 'ADI', 'GILD', 'VRTX',
            'ADP', 'REGN', 'PANW', 'MU', 'LRCX', 'PYPL', 'KLAC', 'SNPS', 'CDNS', 'MELI',
            'ASML', 'ABNB', 'MAR', 'ORLY', 'CRWD', 'CSX', 'FTNT', 'ADSK', 'DASH', 'MRVL',
            'WDAY', 'NXPI', 'MNST', 'CHTR', 'PCAR', 'CPRT', 'AEP', 'PAYX', 'ROST', 'MCHP',
            'ODFL', 'KDP', 'FAST', 'DXCM', 'CTAS', 'VRSK', 'EA', 'CTSH', 'IDXX', 'BKR',
            'LULU', 'GEHC', 'EXC', 'XEL', 'CCEP', 'TEAM', 'KHC', 'FANG', 'ZS', 'TTWO',
            'DDOG', 'ON', 'ANSS', 'CSGP', 'CDW', 'BIIB', 'WBD', 'ILMN', 'GFS', 'MDB'
        ]
        return nasdaq_tickers
    except Exception as e:
        print(f"Error fetching NASDAQ tickers: {e}")
        return []


def get_nyse_tickers() -> List[str]:
    """Fetch NYSE ticker symbols."""
    try:
        # Using a predefined list of major NYSE stocks
        nyse_tickers = [
            'JPM', 'V', 'JNJ', 'WMT', 'UNH', 'MA', 'PG', 'HD', 'CVX', 'MRK',
            'ABBV', 'KO', 'BAC', 'PFE', 'LLY', 'TMO', 'ORCL', 'ACN', 'DIS', 'ABT',
            'NKE', 'CRM', 'TMUS', 'VZ', 'DHR', 'WFC', 'PM', 'BMY', 'NEE', 'RTX',
            'SPGI', 'UPS', 'MS', 'LOW', 'T', 'CAT', 'GS', 'BLK', 'LMT', 'BA',
            'AXP', 'DE', 'SCHW', 'ELV', 'PLD', 'SYK', 'BKNG', 'ADI', 'MMC', 'TJX',
            'C', 'AMT', 'CB', 'GILD', 'CI', 'VRTX', 'BDX', 'SO', 'MDLZ', 'ISRG',
            'DUK', 'ZTS', 'PGR', 'CME', 'ITW', 'EOG', 'USB', 'APO', 'TGT', 'HCA',
            'CL', 'NSC', 'BSX', 'MMM', 'PNC', 'AON', 'SLB', 'MCO', 'EMR', 'GD',
            'ICE', 'WM', 'GM', 'F', 'FDX', 'PSA', 'MO', 'COP', 'SHW', 'APD'
        ]
        return nyse_tickers
    except Exception as e:
        print(f"Error fetching NYSE tickers: {e}")
        return []


def get_amex_tickers() -> List[str]:
    """Fetch AMEX ticker symbols."""
    try:
        # Using a predefined list of major AMEX stocks
        amex_tickers = [
            'SPY', 'QQQ', 'IWM', 'EEM', 'GLD', 'SLV', 'XLE', 'XLF', 'XLK', 'XLV',
            'XLI', 'XLP', 'XLY', 'XLU', 'XLB', 'XLRE', 'XLC', 'VXX', 'EWJ', 'EWZ',
            'FXI', 'EFA', 'VWO', 'HYG', 'LQD', 'TLT', 'IEF', 'SHY', 'AGG', 'BND',
            'VNQ', 'IEMG', 'VEA', 'VTI', 'VOO', 'IVV', 'VTV', 'VUG', 'VIG', 'VYM'
        ]
        return amex_tickers
    except Exception as e:
        print(f"Error fetching AMEX tickers: {e}")
        return []


def get_all_us_tickers() -> List[str]:
    """Fetch all US market ticker symbols."""
    nasdaq = get_nasdaq_tickers()
    nyse = get_nyse_tickers()
    amex = get_amex_tickers()
    
    # Combine and remove duplicates
    all_tickers = list(set(nasdaq + nyse + amex))
    return sorted(all_tickers)


def get_tickers_by_market(market: str) -> List[str]:
    """
    Get ticker symbols based on market selection.
    
    Args:
        market: One of ["NASDAQ", "NYSE", "AMEX", "All US Markets"]
    
    Returns:
        List of ticker symbols
    """
    market_map = {
        "NASDAQ": get_nasdaq_tickers,
        "NYSE": get_nyse_tickers,
        "AMEX": get_amex_tickers,
        "All US Markets": get_all_us_tickers
    }
    
    if market in market_map:
        return market_map[market]()
    else:
        return []
