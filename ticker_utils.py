"""
Utility functions for fetching comprehensive stock ticker lists from various exchanges.
Uses NASDAQ FTP service for complete US market coverage.
"""
import pandas as pd
import yfinance as yf
from typing import List
import time
import requests
from io import StringIO
import urllib.request


def get_nasdaq_listed_stocks() -> List[str]:
    """
    Fetch all NASDAQ-listed stocks from NASDAQ's official FTP server.
    Returns comprehensive list of all NASDAQ stocks (typically 3000+).
    """
    try:
        url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
        
        print("   Downloading from NASDAQ FTP server...")
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        
        # Parse the pipe-delimited file
        lines = content.strip().split('\n')
        tickers = []
        
        for line in lines[1:]:  # Skip header
            if '|' in line:
                parts = line.split('|')
                ticker = parts[0].strip()
                # Filter out test symbols and invalid tickers
                if ticker and not ticker.startswith('$') and ticker != 'Symbol':
                    # Check if it's a valid ticker (not the file footer)
                    if ticker and len(ticker) <= 5 and ticker.replace('-', '').replace('.', '').isalnum():
                        tickers.append(ticker)
        
        print(f"✓ Fetched {len(tickers)} NASDAQ-listed stocks from FTP")
        return tickers
        
    except Exception as e:
        print(f"✗ Error fetching NASDAQ FTP data: {e}")
        return []


def get_other_listed_stocks() -> List[str]:
    """
    Fetch all NYSE and other exchange-listed stocks from NASDAQ's FTP server.
    Returns comprehensive list of non-NASDAQ stocks (typically 3000+).
    """
    try:
        url = "ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt"
        
        print("   Downloading from NASDAQ FTP server...")
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        
        # Parse the pipe-delimited file
        lines = content.strip().split('\n')
        tickers = []
        
        for line in lines[1:]:  # Skip header
            if '|' in line:
                parts = line.split('|')
                ticker = parts[0].strip()
                # Filter out test symbols and invalid tickers
                if ticker and not ticker.startswith('$') and ticker != 'ACT Symbol':
                    # Check if it's a valid ticker
                    if ticker and len(ticker) <= 5 and ticker.replace('-', '').replace('.', '').isalnum():
                        tickers.append(ticker)
        
        print(f"✓ Fetched {len(tickers)} NYSE/Other-listed stocks from FTP")
        return tickers
        
    except Exception as e:
        print(f"✗ Error fetching NYSE/Other FTP data: {e}")
        return []


def get_sp500_tickers() -> List[str]:
    """
    Fetch S&P 500 ticker symbols from Wikipedia.
    Returns approximately 500 stocks.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        tables = pd.read_html(StringIO(response.text))
        sp500_df = tables[0]
        tickers = sp500_df['Symbol'].tolist()
        
        # Clean tickers
        cleaned_tickers = [str(ticker).replace('.', '-') for ticker in tickers if pd.notna(ticker)]
        
        print(f"✓ Fetched {len(cleaned_tickers)} S&P 500 tickers")
        return cleaned_tickers
        
    except Exception as e:
        print(f"✗ Error fetching S&P 500 tickers: {e}")
        return []


def get_nasdaq100_tickers() -> List[str]:
    """
    Fetch NASDAQ-100 ticker symbols from Wikipedia.
    Returns approximately 100 stocks.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        tables = pd.read_html(StringIO(response.text))
        
        for table in tables:
            if 'Ticker' in table.columns:
                tickers = table['Ticker'].tolist()
                cleaned_tickers = [str(ticker).replace('.', '-') for ticker in tickers if pd.notna(ticker)]
                print(f"✓ Fetched {len(cleaned_tickers)} NASDAQ-100 tickers")
                return cleaned_tickers
        
        print("✗ Could not find NASDAQ-100 ticker table")
        return []
        
    except Exception as e:
        print(f"✗ Error fetching NASDAQ-100 tickers: {e}")
        return []


def get_dow30_tickers() -> List[str]:
    """
    Fetch Dow Jones Industrial Average (DJIA) 30 ticker symbols.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        tables = pd.read_html(StringIO(response.text))
        
        for table in tables:
            if 'Symbol' in table.columns and len(table) == 30:
                tickers = table['Symbol'].tolist()
                cleaned_tickers = [str(ticker).replace('.', '-') for ticker in tickers if pd.notna(ticker)]
                print(f"✓ Fetched {len(cleaned_tickers)} Dow 30 tickers")
                return cleaned_tickers
        
        print("✗ Could not find Dow 30 ticker table")
        return []
        
    except Exception as e:
        print(f"✗ Error fetching Dow 30 tickers: {e}")
        return []


def get_russell2000_tickers() -> List[str]:
    """
    Fetch Russell 2000 ticker symbols.
    Note: Comprehensive Russell 2000 data is not freely available.
    This returns an empty list as a placeholder.
    """
    print("ℹ Russell 2000 comprehensive data not available from free sources")
    print("  Use 'All US Markets' for comprehensive coverage instead")
    return []


def get_nasdaq_tickers() -> List[str]:
    """
    Fetch all NASDAQ-listed stocks using FTP source.
    Returns comprehensive NASDAQ coverage (3000+ stocks).
    """
    print("\n[NASDAQ] Fetching comprehensive NASDAQ listings...")
    return get_nasdaq_listed_stocks()


def get_nyse_tickers() -> List[str]:
    """
    Fetch NYSE-listed stocks using FTP source.
    Returns comprehensive NYSE coverage (2000+ stocks).
    """
    print("\n[NYSE] Fetching comprehensive NYSE listings...")
    return get_other_listed_stocks()


def get_amex_tickers() -> List[str]:
    """
    Fetch AMEX ticker symbols.
    Using curated list of major ETFs.
    """
    amex_tickers = [
        'SPY', 'QQQ', 'IWM', 'EEM', 'GLD', 'SLV', 'XLE', 'XLF', 'XLK', 'XLV',
        'XLI', 'XLP', 'XLY', 'XLU', 'XLB', 'XLRE', 'XLC', 'VXX', 'EWJ', 'EWZ',
        'FXI', 'EFA', 'VWO', 'HYG', 'LQD', 'TLT', 'IEF', 'SHY', 'AGG', 'BND',
        'VNQ', 'IEMG', 'VEA', 'VTI', 'VOO', 'IVV', 'VTV', 'VUG', 'VIG', 'VYM'
    ]
    print(f"✓ Using curated AMEX ETF list: {len(amex_tickers)} tickers")
    return amex_tickers


def get_comprehensive_us_tickers() -> List[str]:
    """
    Fetch comprehensive US market ticker symbols from NASDAQ FTP sources.
    Combines NASDAQ-listed and other exchange-listed stocks.
    Returns 5000-7000+ unique tickers covering all major US exchanges.
    """
    print("\n" + "="*70)
    print("FETCHING COMPREHENSIVE US MARKET TICKERS")
    print("Using NASDAQ FTP Service for Complete Market Coverage")
    print("="*70 + "\n")
    
    all_tickers = []
    
    # Get all NASDAQ-listed stocks from FTP (3000+)
    print("[1/3] Fetching all NASDAQ-listed stocks...")
    nasdaq_listed = get_nasdaq_listed_stocks()
    if nasdaq_listed:
        all_tickers.extend(nasdaq_listed)
        print(f"      ✓ Added {len(nasdaq_listed)} NASDAQ stocks\n")
    
    # Get all NYSE and other exchange-listed stocks from FTP (3000+)
    print("[2/3] Fetching all NYSE and other exchange-listed stocks...")
    other_listed = get_other_listed_stocks()
    if other_listed:
        all_tickers.extend(other_listed)
        print(f"      ✓ Added {len(other_listed)} NYSE/Other stocks\n")
    
    # Add major ETFs
    print("[3/3] Adding major ETFs...")
    amex = get_amex_tickers()
    if amex:
        all_tickers.extend(amex)
        print(f"      ✓ Added {len(amex)} ETFs\n")
    
    # Remove duplicates and clean
    unique_tickers = list(set(all_tickers))
    
    # Filter out invalid tickers
    valid_tickers = []
    for ticker in unique_tickers:
        if isinstance(ticker, str):
            ticker = ticker.strip()
            # Accept tickers that are 1-5 characters
            if 1 <= len(ticker) <= 5:
                # Allow alphanumeric with optional dash or dot
                clean_ticker = ticker.replace('-', '').replace('.', '')
                if clean_ticker.isalnum():
                    valid_tickers.append(ticker)
    
    valid_tickers = sorted(valid_tickers)
    
    print("="*70)
    print(f"✓ TOTAL UNIQUE VALID TICKERS: {len(valid_tickers)}")
    print(f"  This represents comprehensive coverage of US stock markets")
    print("="*70 + "\n")
    
    return valid_tickers


def get_all_us_tickers() -> List[str]:
    """
    Fetch all US market ticker symbols with comprehensive coverage.
    """
    return get_comprehensive_us_tickers()


def get_tickers_by_market(market: str) -> List[str]:
    """
    Get ticker symbols based on market selection.
    
    Args:
        market: One of ["S&P 500", "NASDAQ", "NYSE", "AMEX", "Russell 2000", "Dow 30", "All US Markets"]
    
    Returns:
        List of ticker symbols
    """
    market_map = {
        "S&P 500": get_sp500_tickers,
        "NASDAQ": get_nasdaq_tickers,
        "NYSE": get_nyse_tickers,
        "AMEX": get_amex_tickers,
        "Russell 2000": get_russell2000_tickers,
        "Dow 30": get_dow30_tickers,
        "All US Markets": get_all_us_tickers
    }
    
    if market in market_map:
        return market_map[market]()
    else:
        print(f"✗ Unknown market: {market}")
        print(f"   Available options: {list(market_map.keys())}")
        return []


# Test function
if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING COMPREHENSIVE TICKER FETCHING")
    print("="*70 + "\n")
    
    print("\n--- TEST 1: S&P 500 (Wikipedia) ---")
    sp500 = get_sp500_tickers()
    print(f"Count: {len(sp500)}")
    if sp500:
        print(f"Sample: {sp500[:15]}\n")
    
    print("\n--- TEST 2: NASDAQ-100 (Wikipedia) ---")
    nasdaq100 = get_nasdaq100_tickers()
    print(f"Count: {len(nasdaq100)}")
    if nasdaq100:
        print(f"Sample: {nasdaq100[:15]}\n")
    
    print("\n--- TEST 3: NASDAQ All Stocks (FTP) ---")
    nasdaq_all = get_nasdaq_listed_stocks()
    print(f"Count: {len(nasdaq_all)}")
    if nasdaq_all:
        print(f"Sample (first 15): {nasdaq_all[:15]}")
        print(f"Sample (last 15): {nasdaq_all[-15:]}\n")
    
    print("\n--- TEST 4: NYSE/Other All Stocks (FTP) ---")
    nyse_all = get_other_listed_stocks()
    print(f"Count: {len(nyse_all)}")
    if nyse_all:
        print(f"Sample (first 15): {nyse_all[:15]}")
        print(f"Sample (last 15): {nyse_all[-15:]}\n")
    
    print("\n--- TEST 5: All US Markets (Comprehensive FTP) ---")
    all_us = get_all_us_tickers()
    print(f"\nFinal Count: {len(all_us)}")
    if all_us:
        print(f"Sample (first 20): {all_us[:20]}")
        print(f"Sample (middle 20): {all_us[len(all_us)//2:len(all_us)//2+20]}")
        print(f"Sample (last 20): {all_us[-20:]}")
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print(f"Total tickers available for scanning: {len(all_us)}")
    print("="*70 + "\n")
