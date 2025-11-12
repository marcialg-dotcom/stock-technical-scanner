"""
Stock Scanner Dashboard - Streamlit Application
Scans U.S. stocks based on technical criteria
"""
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import time
from ticker_utils import get_tickers_by_market

# Import scanner libraries
from scanners.scan_price_surge import scan_price_surge
from scanners.scan_upward_gap import scan_upward_gap
from scanners.scan_continuous_uptrend import scan_continuous_uptrend
from scanners.scan_volume_breakout import scan_volume_breakout


# Page configuration
st.set_page_config(
    page_title="Stock Technical Scanner",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


def fetch_stock_data(ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker.
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date for data fetch
        end_date: End date for data fetch
    
    Returns:
        DataFrame with stock data or None if error
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty or len(data) < 10:
            return None
        
        return data
    except Exception as e:
        return None


# Scan functions are now imported from scanners package
# See scanners/scan_price_surge.py
# See scanners/scan_upward_gap.py
# See scanners/scan_continuous_uptrend.py
# See scanners/scan_volume_breakout.py


def perform_scans(tickers: List[str], start_date: datetime, end_date: datetime, 
                  scan_start_date: datetime,
                  price_surge_threshold: float = 0.05,
                  upward_gap_threshold: float = 0.01,
                  uptrend_min_days: int = 4,
                  volume_breakout_threshold: float = 0.10) -> Dict[str, pd.DataFrame]:
    """
    Perform all four scans on the given tickers.
    
    Args:
        tickers: List of ticker symbols
        start_date: Start date for data fetch (includes buffer for calculations)
        end_date: End date for data fetch
        scan_start_date: Actual start date for scan results
        price_surge_threshold: Threshold for price surge scan (default 0.05 = 5%)
        upward_gap_threshold: Threshold for upward gap scan (default 0.01 = 1%)
        uptrend_min_days: Minimum days for continuous uptrend (default 4)
        volume_breakout_threshold: Threshold for volume breakout (default 0.10 = 10%)
    
    Returns:
        Dictionary with scan results
    """
    scan_a_results = []
    scan_b_results = []
    scan_c_results = []
    scan_d_results = []
    
    # Track which tickers meet each criterion
    tickers_with_surge = set()
    tickers_with_gap = set()
    tickers_with_uptrend = set()
    tickers_with_volume = set()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_tickers = len(tickers)
    
    for i, ticker in enumerate(tickers):
        # Check if stop was requested
        if st.session_state.get('stop_requested', False):
            status_text.text(f"⏹️ Scan stopped by user at {i}/{total_tickers} stocks")
            st.warning(f"⚠️ Scan interrupted! Processed {i} out of {total_tickers} stocks.")
            break
        
        # Update progress
        progress = (i + 1) / total_tickers
        progress_bar.progress(progress)
        status_text.text(f"Scanning {ticker}... ({i + 1}/{total_tickers})")
        
        # Fetch data
        data = fetch_stock_data(ticker, start_date, end_date)
        
        if data is None:
            continue
        
        # Filter data to scan period only for results
        # Ensure scan_start_date is timezone-aware if data.index is timezone-aware
        scan_start_compare = pd.Timestamp(scan_start_date)
        if data.index.tz is not None:
            scan_start_compare = scan_start_compare.tz_localize(data.index.tz)
        scan_data = data[data.index >= scan_start_compare]
        
        # Perform scans with custom parameters
        surge_results = scan_price_surge(scan_data, threshold=price_surge_threshold)
        if surge_results:
            tickers_with_surge.add(ticker)
        for date, pct_change, price in surge_results:
            scan_a_results.append({
                'Ticker': ticker,
                'Date': date,
                'Price Change (%)': f"{pct_change:.2f}",
                'Close Price': f"${price:.2f}",
                'Volume': int(scan_data.loc[date, 'Volume']) if date in scan_data.index else 'N/A'
            })
        
        gap_results = scan_upward_gap(scan_data, threshold=upward_gap_threshold)
        if gap_results:
            tickers_with_gap.add(ticker)
        for date, gap_pct, price in gap_results:
            scan_b_results.append({
                'Ticker': ticker,
                'Date': date,
                'Gap (%)': f"{gap_pct:.2f}",
                'Open Price': f"${price:.2f}",
                'Volume': int(scan_data.loc[date, 'Volume']) if date in scan_data.index else 'N/A'
            })
        
        uptrend_results = scan_continuous_uptrend(scan_data, min_days=uptrend_min_days)
        if uptrend_results:
            tickers_with_uptrend.add(ticker)
        for date, num_days, price in uptrend_results:
            scan_c_results.append({
                'Ticker': ticker,
                'End Date': date,
                'Consecutive Days': num_days,
                'Close Price': f"${price:.2f}",
                'Volume': int(scan_data.loc[date, 'Volume']) if date in scan_data.index else 'N/A'
            })
        
        volume_results = scan_volume_breakout(data, threshold=volume_breakout_threshold)
        # Filter volume results to scan period
        volume_found = False
        for date, volume_ratio, volume in volume_results:
            date_compare = pd.Timestamp(date)
            if data.index.tz is not None and date_compare.tz is None:
                date_compare = date_compare.tz_localize(data.index.tz)
            if date_compare >= scan_start_compare:
                volume_found = True
                scan_d_results.append({
                    'Ticker': ticker,
                    'Date': date,
                    'Volume Increase (%)': f"{volume_ratio:.2f}",
                    'Volume': int(volume),
                    'Price': f"${scan_data.loc[date, 'Close']:.2f}" if date in scan_data.index else 'N/A'
                })
        if volume_found:
            tickers_with_volume.add(ticker)
        
        # Add small delay to avoid rate limiting
        time.sleep(0.1)
    
    progress_bar.empty()
    status_text.empty()
    
    # Find stocks that meet ALL four criteria
    all_criteria_tickers = (tickers_with_surge & tickers_with_gap & 
                           tickers_with_uptrend & tickers_with_volume)
    
    # Create combined results
    combined_results = []
    for ticker in sorted(all_criteria_tickers):
        # Get the most recent data for this ticker
        latest_price = 'N/A'
        latest_volume = 'N/A'
        
        # Try to get latest info from scan results
        for result in scan_a_results:
            if result['Ticker'] == ticker:
                latest_price = result['Close Price']
                break
        
        for result in scan_d_results:
            if result['Ticker'] == ticker:
                latest_volume = result['Volume']
                break
        
        combined_results.append({
            'Ticker': ticker,
            'Price': latest_price,
            'Volume': latest_volume,
            'Criteria Met': 'All 4',
            'Yahoo Finance': f"https://finance.yahoo.com/quote/{ticker}"
        })
    
    return {
        f'Scan A: Price Surge (>{price_surge_threshold*100:.1f}%)': pd.DataFrame(scan_a_results),
        f'Scan B: Upward Gap (>{upward_gap_threshold*100:.1f}%)': pd.DataFrame(scan_b_results),
        f'Scan C: Continuous Uptrend (≥{uptrend_min_days} days)': pd.DataFrame(scan_c_results),
        f'Scan D: Volume Breakout (>{volume_breakout_threshold*100:.0f}%)': pd.DataFrame(scan_d_results),
        'Combined: All 4 Criteria': pd.DataFrame(combined_results)
    }


def main():
    """Main application function."""
    
    # Title
    st.title("📈 Stock Technical Scanner")
    st.markdown("Scan U.S. stocks based on technical criteria")
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Scan Parameters")
        
        # Input 1: Number of Days to Scan
        scan_days = st.number_input(
            "Number of Days to Scan",
            min_value=5,
            max_value=60,
            value=20,
            step=1,
            help="Number of trading days to scan for signals"
        )
        
        # Input 2: Stock Market
        market = st.selectbox(
            "Stock Market",
            ["S&P 500", "NASDAQ", "NYSE", "AMEX", "Russell 2000", "All US Markets"],
            help="Select which market to scan. S&P 500 (~500 stocks), NASDAQ-100 (~100), Russell 2000 (~2000), All US Markets (~2500+)"
        )
        
        # Input 3: Current Date
        current_date = st.date_input(
            "Current Date",
            value=datetime.now(),
            help="End date for the scan period"
        )
        
        # Input 4: Alphabetical Filter
        st.markdown("---")
        st.subheader("🔤 Ticker Filter (Optional)")
        
        enable_alpha_filter = st.checkbox(
            "Enable Alphabetical Filtering",
            value=False,
            help="Filter tickers by starting letter to reduce scan size"
        )
        
        if enable_alpha_filter:
            alpha_range = st.selectbox(
                "Ticker Range",
                [
                    "All (A-Z)",
                    "A-C",
                    "D-F",
                    "G-I",
                    "J-L",
                    "M-O",
                    "P-R",
                    "S-U",
                    "V-Z"
                ],
                help="Select which alphabetical range of tickers to scan"
            )
        else:
            alpha_range = "All (A-Z)"
        
        st.markdown("---")
        
        # Input 5: Scan Criteria Parameters
        st.subheader("⚙️ Scan Criteria Settings")
        
        # Scan A: Price Surge threshold
        price_surge_pct = st.number_input(
            "Price Surge Threshold (%)",
            min_value=1.0,
            max_value=20.0,
            value=5.0,
            step=0.5,
            help="Minimum single-day price increase percentage (default: 5%)"
        )
        
        # Scan B: Upward Gap threshold
        upward_gap_pct = st.number_input(
            "Upward Gap Threshold (%)",
            min_value=0.5,
            max_value=10.0,
            value=1.0,
            step=0.5,
            help="Minimum gap percentage above previous close (default: 1%)"
        )
        
        # Scan C: Continuous Uptrend days
        uptrend_days = st.number_input(
            "Continuous Uptrend Days",
            min_value=2,
            max_value=20,
            value=4,
            step=1,
            help="Minimum consecutive days of higher closes (default: 4)"
        )
        
        # Scan D: Volume Breakout threshold
        volume_breakout_pct = st.number_input(
            "Volume Breakout Threshold (%)",
            min_value=5.0,
            max_value=50.0,
            value=10.0,
            step=5.0,
            help="Minimum volume increase above 50-day average (default: 10%)"
        )
        
        st.markdown("---")
        
        # Scan button
        scan_button = st.button("🚀 Start Scan", type="primary", use_container_width=True)
        
        # Stop button (will be shown during scan)
        if 'scanning' not in st.session_state:
            st.session_state.scanning = False
        
        if st.session_state.scanning:
            stop_button = st.button("⏹️ Stop Scan", type="secondary", use_container_width=True)
            if stop_button:
                st.session_state.stop_requested = True
                st.warning("Stop requested. Scan will halt after current stock...")
        else:
            st.session_state.stop_requested = False
    
    # Main area
    if scan_button:
        # Calculate dates
        end_date = datetime.combine(current_date, datetime.min.time())
        start_date = end_date - timedelta(days=scan_days + 55)  # Add buffer for 50-day volume calculation
        scan_start_date = end_date - timedelta(days=scan_days)
        
        # Set scanning state
        st.session_state.scanning = True
        st.session_state.stop_requested = False
        
        # Get tickers
        st.info(f"Fetching {market} tickers...")
        tickers = get_tickers_by_market(market)
        
        if not tickers:
            st.error("No tickers found for the selected market.")
            st.session_state.scanning = False
            return
        
        # Apply alphabetical filter if enabled
        if alpha_range != "All (A-Z)":
            original_count = len(tickers)
            
            # Define range mapping
            range_map = {
                "A-C": ('A', 'D'),
                "D-F": ('D', 'G'),
                "G-I": ('G', 'J'),
                "J-L": ('J', 'M'),
                "M-O": ('M', 'P'),
                "P-R": ('P', 'S'),
                "S-U": ('S', 'V'),
                "V-Z": ('V', '[')
            }
            
            if alpha_range in range_map:
                start_letter, end_letter = range_map[alpha_range]
                tickers = [t for t in tickers if start_letter <= t[0].upper() < end_letter]
                st.info(f"🔤 Alphabetical Filter Applied: {alpha_range}")
                st.info(f"   Filtered from {original_count} to {len(tickers)} tickers")
        
        st.success(f"✓ Found {len(tickers)} tickers to scan")
        
        # Display date range
        st.info(f"📅 Scan Period: {scan_start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        st.info(f"📊 Data Fetch Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} (includes 55-day buffer)")
        
        # Perform scans with user-defined parameters
        st.subheader("Scanning in Progress...")
        results = perform_scans(
            tickers, 
            start_date, 
            end_date, 
            scan_start_date,
            price_surge_threshold=price_surge_pct / 100,  # Convert % to decimal
            upward_gap_threshold=upward_gap_pct / 100,    # Convert % to decimal
            uptrend_min_days=uptrend_days,
            volume_breakout_threshold=volume_breakout_pct / 100  # Convert % to decimal
        )
        
        # Reset scanning state
        st.session_state.scanning = False
        st.session_state.stop_requested = False
        
        # Display results
        st.success("✅ Scan Complete!")
        
        # Summary statistics
        st.subheader("📊 Summary Statistics")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Price Surge Signals", len(results['Scan A: Price Surge (>5%)']))
        with col2:
            st.metric("Upward Gap Signals", len(results['Scan B: Upward Gap']))
        with col3:
            st.metric("Uptrend Signals", len(results['Scan C: Continuous Uptrend (≥4 days)']))
        with col4:
            st.metric("Volume Breakout Signals", len(results['Scan D: Volume Breakout']))
        with col5:
            st.metric("⭐ All 4 Criteria", len(results['Combined: All 4 Criteria']), delta="Premium Picks")
        
        # Display results in tabs
        st.subheader("🔍 Detailed Results")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "⭐ All 4 Criteria",
            "Scan A: Price Surge",
            "Scan B: Upward Gap",
            "Scan C: Continuous Uptrend",
            "Scan D: Volume Breakout"
        ])
        
        with tab1:
            st.markdown("**🎯 Premium Picks: Stocks Meeting ALL Four Criteria**")
            st.markdown("These stocks show strong signals across all technical indicators:")
            st.markdown("- ✅ Price Surge (>5%)")
            st.markdown("- ✅ Upward Gap (>1%)")
            st.markdown("- ✅ Continuous Uptrend (≥4 days)")
            st.markdown("- ✅ Volume Breakout (>10% above average)")
            st.markdown("---")
            
            df_combined = results['Combined: All 4 Criteria']
            if not df_combined.empty:
                st.success(f"🎉 Found {len(df_combined)} stocks meeting all criteria!")
                st.dataframe(df_combined, use_container_width=True)
                
                # Download button for combined results
                csv_combined = df_combined.to_csv(index=False)
                st.download_button(
                    label="📥 Download Premium Picks as CSV",
                    data=csv_combined,
                    file_name=f"all_criteria_{current_date}.csv",
                    mime="text/csv",
                    type="primary"
                )
                
                # Also create a simple ticker-only CSV
                ticker_only_csv = df_combined[['Ticker']].to_csv(index=False)
                st.download_button(
                    label="📋 Download Ticker List Only",
                    data=ticker_only_csv,
                    file_name=f"tickers_all_criteria_{current_date}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No stocks found meeting all four criteria in this scan period.")
                st.info("💡 Tip: Try increasing the scan period or selecting 'All US Markets' for better results.")
        
        with tab2:
            st.markdown("**Stocks with single-day price increase >5%**")
            df_a = results['Scan A: Price Surge (>5%)']
            if not df_a.empty:
                # Add Yahoo Finance links
                df_a['Yahoo Finance'] = df_a['Ticker'].apply(
                    lambda x: f"https://finance.yahoo.com/quote/{x}"
                )
                st.dataframe(df_a, use_container_width=True)
                
                # Download button
                csv_a = df_a.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_a,
                    file_name=f"price_surge_{current_date}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No stocks found matching this criterion.")
        
        with tab2:
            st.markdown("**Stocks with upward gap >1%**")
            df_b = results['Scan B: Upward Gap']
            if not df_b.empty:
                df_b['Yahoo Finance'] = df_b['Ticker'].apply(
                    lambda x: f"https://finance.yahoo.com/quote/{x}"
                )
                st.dataframe(df_b, use_container_width=True)
                
                csv_b = df_b.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_b,
                    file_name=f"upward_gap_{current_date}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No stocks found matching this criterion.")
        
        with tab3:
            st.markdown("**Stocks with continuous uptrend ≥4 days**")
            df_c = results['Scan C: Continuous Uptrend (≥4 days)']
            if not df_c.empty:
                df_c['Yahoo Finance'] = df_c['Ticker'].apply(
                    lambda x: f"https://finance.yahoo.com/quote/{x}"
                )
                st.dataframe(df_c, use_container_width=True)
                
                csv_c = df_c.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_c,
                    file_name=f"continuous_uptrend_{current_date}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No stocks found matching this criterion.")
        
        with tab4:
            st.markdown("**Stocks with volume >10% above 50-day average**")
            df_d = results['Scan D: Volume Breakout']
            if not df_d.empty:
                df_d['Yahoo Finance'] = df_d['Ticker'].apply(
                    lambda x: f"https://finance.yahoo.com/quote/{x}"
                )
                st.dataframe(df_d, use_container_width=True)
                
                csv_d = df_d.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_d,
                    file_name=f"volume_breakout_{current_date}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No stocks found matching this criterion.")
    
    else:
        # Initial state - show instructions
        st.markdown("""
        ### Welcome to the Stock Technical Scanner! 👋
        
        This dashboard helps you identify stocks based on four technical criteria:
        
        1. **Price Surge (>5%)**: Stocks with single-day price increase exceeding 5%
        2. **Upward Gap**: Stocks that opened more than 1% above previous close
        3. **Continuous Uptrend**: Stocks with 4 or more consecutive days of higher closes
        4. **Volume Breakout**: Stocks with volume exceeding 10% above their 50-day average
        
        ### ⭐ NEW: Premium Picks Feature!
        The scanner now identifies **elite stocks that meet ALL FOUR criteria** simultaneously - 
        these are the strongest technical signals!
        
        #### How to Use:
        1. Set your scan parameters in the left sidebar
        2. Click the **Start Scan** button
        3. Check the **"⭐ All 4 Criteria"** tab for premium picks
        4. Download results as CSV files (full data or ticker list only)
        
        #### Tips:
        - Longer scan periods provide more signals but take longer to process
        - "All US Markets" option scans the most stocks but is slowest
        - The "All 4 Criteria" tab shows only the highest-quality signals
        - Results include clickable links to Yahoo Finance for each stock
        """)
        
        # Display sample data structure
        st.subheader("📋 Sample Output Format")
        
        sample_data = pd.DataFrame({
            'Ticker': ['AAPL', 'MSFT', 'GOOGL'],
            'Date': ['2024-01-15', '2024-01-16', '2024-01-17'],
            'Signal Strength': ['6.5%', '5.8%', '7.2%'],
            'Price': ['$185.50', '$405.20', '$142.80'],
            'Volume': ['75,234,100', '28,456,200', '32,145,800']
        })
        
        st.dataframe(sample_data, use_container_width=True)


if __name__ == "__main__":
    main()
