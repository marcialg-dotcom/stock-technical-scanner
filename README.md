# Stock Technical Scanner Dashboard

A Streamlit-based web application for scanning U.S. stocks based on technical criteria.

## Features

The dashboard performs four types of technical scans:

1. **Scan A: Price Surge (>5%)** - Identifies stocks with single-day price increases exceeding 5%
2. **Scan B: Upward Gap** - Finds stocks that opened more than 1% above the previous day's close
3. **Scan C: Continuous Uptrend (≥4 days)** - Detects stocks with 4 or more consecutive days of higher closes
4. **Scan D: Volume Breakout** - Identifies stocks with volume exceeding 10% above their 50-day average

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. The dashboard will open in your default web browser

3. Configure scan parameters in the left sidebar:
   - **Number of Days to Scan**: Set the lookback period (5-60 days)
   - **Stock Market**: Choose from NASDAQ, NYSE, AMEX, or All US Markets
   - **Current Date**: Set the end date for the scan

4. Click the **Start Scan** button to begin scanning

5. View results in the tabbed interface:
   - Each tab shows stocks matching a specific criterion
   - Results include ticker symbol, date, signal strength, price, and volume
   - Yahoo Finance links are provided for each stock

6. Download results as CSV files using the download buttons

## Technical Details

### Data Source
- Uses `yfinance` library to fetch historical stock data from Yahoo Finance

### Scan Logic

**Price Surge:**
```python
pct_change = (current_close - previous_close) / previous_close
if pct_change > 0.05:  # 5% threshold
    # Record signal
```

**Upward Gap:**
```python
if current_open > previous_close * 1.01:  # 1% gap threshold
    # Record signal
```

**Continuous Uptrend:**
```python
# Check for consecutive days where close_day(n) < close_day(n+1)
if consecutive_days >= 4:
    # Record signal
```

**Volume Breakout:**
```python
avg_volume_50d = mean(volume[-51:-1])
if current_volume > avg_volume_50d * 1.10:  # 10% above average
    # Record signal
```

### Date Range Calculation
- The system fetches data starting from `current_date - (scan_days + 55)` days
- The extra 55 days provide buffer for calculating the 50-day volume average
- Only signals within the specified scan period are displayed

## Notes

- The application includes a predefined list of major stocks from each exchange
- For production use, consider implementing a more comprehensive ticker source
- API rate limiting is handled with small delays between requests
- Stocks with insufficient data are automatically skipped

## File Structure

```
stock_scanner/
├── app.py              # Main Streamlit application
├── ticker_utils.py     # Utility functions for fetching ticker lists
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Requirements

- Python 3.8+
- streamlit
- yfinance
- pandas

## License

This project is provided as-is for educational and personal use.
