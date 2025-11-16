import streamlit as st
import pandas as pd
import yfinance as yf
from fredapi import Fred
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
# This must be the first command in your app
st.set_page_config(
    page_title="Tech Sector Alpha Monitor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- API KEYS & TICKERS ---
FRED_API_KEY = st.secrets["FRED_API_KEY"]
fred = Fred(api_key=FRED_API_KEY)

# The "Magnificent 7" 
TICKER_LIST = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META']

# --- HELPER FUNCTIONS (We'll build these tomorrow) ---
@st.cache_data(ttl="1h")  # Cache data for 1 hour
def get_stock_data(ticker):
    """Fetches stock data from yfinance."""
    # TODO: Fetch historical price data (1y)
    # TODO: Fetch company info (info['longBusinessSummary'])
    # TODO: Fetch key ratios (info['trailingPE'], info['returnOnEquity'], etc.)
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1y")
        info = stock.info
        return history, info
    except Exception as e:
        st.error(f"Error fetching data from yfinance")
        return pd.DataFrame(),{}

@st.cache_data(ttl="6h")  # Cache data for 6 hours
def get_macro_data():
    """
    Fetches 10-Year Treasury Yield AND Inflation (CPI) from FRED.
    We fetch both, then return them together in a dictionary.
    """
    try:
        # 'DGS10' is the series ID for the 10-Year Treasury
        dgs10data = fred.get_series('DGS10', start_date='2019-01-01')
        
        # 'CPIAUCSL' is the standard ID for US CPI (Inflation)
        cpiData = fred.get_series('CPIAUCSL', start_date='2019-01-01')
        
        # Return both in a single dictionary
        return {
            'dgs10': dgs10data,
            'cpi': cpiData
        }
    except Exception as e:
        st.error(f"Error fetching FRED data {e}")
        return {} # Return an empty dictionary on error
    


# --- UI LAYOUT ---

# --- Sidebar ---
st.sidebar.title("Analyst Note")
st.sidebar.info(
    """
    **Thesis:** While high-growth tech (e.g., NVDA) continues to dominate headlines,
    the current high interest rate environment (see Macro tab) historically
    compresses valuations for "long-duration" assets.
    
    This dashboard analyses which 'Magnificent 7' stocks are priced for perfection
    vs. which may offer more reasonable risk-adjusted returns based on
    P/E-to-Growth and ROE.
    """
)
st.sidebar.markdown("---")
st.sidebar.header("Controls")
# TODO: Add a multi-select for tickers
# selected_tickers = st.sidebar.multiselect("Select Tickers", TICKER_LIST, default=['AAPL', 'MSFT', 'NVDA'])


# --- Main Page ---
st.title("📈 US Tech & AI Sector Investment Dashboard")
st.caption(f"Tracking: {', '.join(TICKER_LIST)}")

# Create the 3 tabs
tab1, tab2, tab3 = st.tabs(
    ["1. The Macro Backdrop", "2. The Valuation Matrix", "3. Ticker Deep Dive"] 
)

with tab1:
    st.header("The Macro Backdrop: Rates vs. Tech")
    st.markdown("""
    This chart shows the relationship between tech valuations (represented by the NASDAQ-100) 
    and interest rates (represented by the US 10-Year Treasury Yield).
    Historically, rising rates put downward pressure on tech stocks.
    """)
    
    # Call the function and get the dictionary
    macro_data_dict = get_macro_data()

    if macro_data_dict:
        # Plot DGS10
        st.subheader("US 10-Year Treasury Yield (DGS10)")
        st.line_chart(macro_data_dict['dgs10'])
        
        # Plot CPI
        st.subheader("US Inflation Rate (CPIAUCSL)")
        st.line_chart(macro_data_dict['cpi'])
    else:
        st.warning("Could not fetch macro data. please check your FRED API Key")

with tab2:
    st.header("The Valuation Matrix: Growth vs. Price")
    st.markdown("""
    This scatter plot identifies which stocks are 'cheap' (Low P/E) vs. 'expensive' (High P/E)
    relative to their growth (Revenue Growth %).
    
    * **Top-Right:** High Growth, High P/E (e.g., NVDA) - *Priced for Perfection*
    * **Bottom-Right:** High Growth, Low P/E - *Potential Bargains (GARP)*
    * **Bottom-Left:** Low Growth, Low P/E - *Value Traps?*
    """)
    
    valuation_data = []
    
    # Show a progress bar while we fetch data for all tickers
    progress_bar = st.progress(0, text="Fetching valuation data...")
    
    for i, ticker in enumerate(TICKER_LIST):
        # We can re-use our existing function!
        history, info = get_stock_data(ticker) 
        
        if info:
            pe = info.get('trailingPE')
            # 'revenueGrowth' is a key yfinance metric (YoY)
            growth = info.get('revenueGrowth') 
            
            # Ensure we have valid, non-zero data to plot
            if pe and growth:
                valuation_data.append({
                    'ticker': ticker,
                    'pe': pe,
                    'growth_pct': growth * 100 # Convert 0.25 -> 25.0
                })
        
        # Update progress bar
        progress_bar.progress((i + 1) / len(TICKER_LIST), text=f"Fetching {ticker}...")
    
    # Remove progress bar when done
    progress_bar.empty() 
    
    if valuation_data:
        # Convert our list of dicts to a Pandas DataFrame
        df_valuation = pd.DataFrame(valuation_data)
        
        # Create the Plotly Express scatter plot
        fig = px.scatter(
            df_valuation, 
            x='pe', 
            y='growth_pct', 
            text='ticker', # Show the ticker symbol on the dot
            hover_name='ticker', # Show ticker on hover
            title='P/E Ratio vs. Revenue Growth (%)'
        )
        
        fig.update_traces(textposition='top center')
        fig.update_layout(
            xaxis_title="P/E Ratio (Trailing)",
            yaxis_title="Revenue Growth (YoY %)"
        )
        
        # Display the chart!
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("Could not fetch enough data to build the valuation matrix.")
    
with tab3:
    st.header("Ticker Deep Dive")
    
    # 1. Add the selectbox to choose a stock
    selected_stock = st.selectbox("Select Stock for Deep Dive", TICKER_LIST)
    
    # 2. As soon as a stock is selected, run the code below
    if selected_stock:
        # 3. Call your function to get the data
        history, info = get_stock_data(selected_stock)
        
        # 4. Check if the 'info' dictionary is populated
        if info and info.get('longName'):
            
            # --- Display Company Info ---
            st.subheader(f"Company: {info.get('longName', selected_stock)}")
            
            col1, col2 = st.columns(2)
            with col1:
                # --- THIS IS THE FIX ---
                # Check if logo_url exists and is not empty before showing it
                logo_url = info.get('logo_url', '')
                if logo_url:
                    st.image(logo_url, width=100)
                else:
                    st.write("*(No logo available)*")
                # --- END OF FIX ---
                
            with col2:
                st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
                st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
                st.markdown(f"**Website:** {info.get('website', 'N/A')}")

            st.markdown("---")
            st.subheader("Business Summary")
            st.write(info.get('longBusinessSummary', 'No summary available.'))
            
            st.markdown("---")
            
            # --- Display Fundamental Ratios ---
            st.subheader("Fundamental Ratios")
            
            col_pe, col_roe, col_debt = st.columns(3)
            
            pe_ratio = info.get('trailingPE')
            roe = info.get('returnOnEquity')
            debt_to_equity = info.get('debtToEquity')

            # Use "N/A" for safety if data is missing
            col_pe.metric("P/E Ratio", f"{pe_ratio:.2f}" if pe_ratio else "N/A")
            col_roe.metric("Return on Equity (ROE)", f"{roe * 100:.2f}%" if roe else "N/A")
            col_debt.metric("Debt-to-Equity", f"{debt_to_equity:.2f}" if debt_to_equity else "N/A")
            
            st.markdown("---")
            
            # --- Display Price Chart ---
            st.subheader("Price Performance (1Y)")
            
            if not history.empty:
                # --- UPGRADE: Switched to a professional Candlestick chart ---
                fig_candle = go.Figure(data=[go.Candlestick(x=history.index,
                                open=history['Open'],
                                high=history['High'],
                                low=history['Low'],
                                close=history['Close'],
                                name=selected_stock)])
                
                fig_candle.update_layout(xaxis_rangeslider_visible=False, title=f"{selected_stock} 1-Year Candlestick Chart")
                st.plotly_chart(fig_candle, use_container_width=True)
                
            else:
                st.warning("No price history found.")
                
        else:
            st.error(f"Could not retrieve data for {selected_stock}. The ticker might be invalid or delisted.")


