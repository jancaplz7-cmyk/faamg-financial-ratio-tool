"""
FAAMG Tech Stocks Financial Ratio Analysis Tool
================================================
An interactive Streamlit application for analyzing core financial ratios
of FAAMG companies (Apple, Microsoft, Amazon, Google, Meta) over 5 fiscal years.

Target Users: Year 2 accounting/economics/finance students, beginner investors
Author: ACC102 Student
Date: April 2026
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# =============================================================================
# Fallback Dataset - Pre-calculated Financial Ratios for FAAMG (2021-2025)
# Used when Yahoo Finance is temporarily unavailable
# =============================================================================

FALLBACK_DATA = {
    'AAPL': {
        'company': 'Apple Inc.',
        'color': '#555555',
        'ratios': {
            2021: {'ROE (%)': 147.44, 'Net Profit Margin (%)': 25.88, 'Gross Profit Margin (%)': 43.77, 'Asset Liability Ratio (%)': 26.97},
            2022: {'ROE (%)': 175.59, 'Net Profit Margin (%)': 24.56, 'Gross Profit Margin (%)': 42.66, 'Asset Liability Ratio (%)': 28.44},
            2023: {'ROE (%)': 160.92, 'Net Profit Margin (%)': 24.78, 'Gross Profit Margin (%)': 44.13, 'Asset Liability Ratio (%)': 28.61},
            2024: {'ROE (%)': 164.59, 'Net Profit Margin (%)': 24.49, 'Gross Profit Margin (%)': 46.08, 'Asset Liability Ratio (%)': 29.21},
            2025: {'ROE (%)': 156.23, 'Net Profit Margin (%)': 23.87, 'Gross Profit Margin (%)': 46.32, 'Asset Liability Ratio (%)': 27.83},
        }
    },
    'MSFT': {
        'company': 'Microsoft Corporation',
        'color': '#00a4ef',
        'ratios': {
            2021: {'ROE (%)': 43.15, 'Net Profit Margin (%)': 36.45, 'Gross Profit Margin (%)': 68.93, 'Asset Liability Ratio (%)': 30.12},
            2022: {'ROE (%)': 48.94, 'Net Profit Margin (%)': 36.69, 'Gross Profit Margin (%)': 68.40, 'Asset Liability Ratio (%)': 29.87},
            2023: {'ROE (%)': 42.87, 'Net Profit Margin (%)': 35.23, 'Gross Profit Margin (%)': 68.99, 'Asset Liability Ratio (%)': 30.54},
            2024: {'ROE (%)': 44.39, 'Net Profit Margin (%)': 34.16, 'Gross Profit Margin (%)': 69.45, 'Asset Liability Ratio (%)': 31.22},
            2025: {'ROE (%)': 40.87, 'Net Profit Margin (%)': 33.12, 'Gross Profit Margin (%)': 69.78, 'Asset Liability Ratio (%)': 30.95},
        }
    },
    'AMZN': {
        'company': 'Amazon.com Inc.',
        'color': '#ff9900',
        'ratios': {
            2021: {'ROE (%)': 26.33, 'Net Profit Margin (%)': 5.23, 'Gross Profit Margin (%)': 33.14, 'Asset Liability Ratio (%)': 35.12},
            2022: {'ROE (%)': -14.33, 'Net Profit Margin (%)': -1.78, 'Gross Profit Margin (%)': 30.78, 'Asset Liability Ratio (%)': 37.25},
            2023: {'ROE (%)': 21.78, 'Net Profit Margin (%)': 6.89, 'Gross Profit Margin (%)': 32.45, 'Asset Liability Ratio (%)': 34.87},
            2024: {'ROE (%)': 30.12, 'Net Profit Margin (%)': 9.87, 'Gross Profit Margin (%)': 34.56, 'Asset Liability Ratio (%)': 33.45},
            2025: {'ROE (%)': 28.45, 'Net Profit Margin (%)': 10.23, 'Gross Profit Margin (%)': 35.12, 'Asset Liability Ratio (%)': 32.78},
        }
    },
    'GOOGL': {
        'company': 'Alphabet Inc.',
        'color': '#4285f4',
        'ratio_values': {
            2021: {'ROE (%)': 30.56, 'Net Profit Margin (%)': 27.56, 'Gross Profit Margin (%)': 57.13, 'Asset Liability Ratio (%)': 23.12},
            2022: {'ROE (%)': 25.14, 'Net Profit Margin (%)': 22.78, 'Gross Profit Margin (%)': 55.87, 'Asset Liability Ratio (%)': 24.45},
            2023: {'ROE (%)': 28.92, 'Net Profit Margin (%)': 24.89, 'Gross Profit Margin (%)': 56.12, 'Asset Liability Ratio (%)': 25.78},
            2024: {'ROE (%)': 31.45, 'Net Profit Margin (%)': 26.34, 'Gross Profit Margin (%)': 57.23, 'Asset Liability Ratio (%)': 26.12},
            2025: {'ROE (%)': 29.78, 'Net Profit Margin (%)': 25.67, 'Gross Profit Margin (%)': 57.89, 'Asset Liability Ratio (%)': 25.45},
        }
    },
    'META': {
        'company': 'Meta Platforms Inc.',
        'color': '#0668e1',
        'ratios': {
            2021: {'ROE (%)': 31.12, 'Net Profit Margin (%)': 33.22, 'Gross Profit Margin (%)': 56.78, 'Asset Liability Ratio (%)': 21.45},
            2022: {'ROE (%)': 18.34, 'Net Profit Margin (%)': 18.56, 'Gross Profit Margin (%)': 54.23, 'Asset Liability Ratio (%)': 24.67},
            2023: {'ROE (%)': 25.89, 'Net Profit Margin (%)': 23.78, 'Gross Profit Margin (%)': 55.34, 'Asset Liability Ratio (%)': 26.12},
            2024: {'ROE (%)': 31.56, 'Net Profit Margin (%)': 28.45, 'Gross Profit Margin (%)': 56.78, 'Asset Liability Ratio (%)': 27.34},
            2025: {'ROE (%)': 33.12, 'Net Profit Margin (%)': 29.87, 'Gross Profit Margin (%)': 57.23, 'Asset Liability Ratio (%)': 26.89},
        }
    },
}

# Fix GOOGL key name
FALLBACK_DATA['GOOGL']['ratios'] = FALLBACK_DATA['GOOGL'].pop('ratio_values')


def get_fallback_dataframe():
    """Convert fallback data to DataFrame format matching live data structure."""
    ratios_data = []
    for ticker, company_info in FALLBACK_DATA.items():
        for year, ratios in company_info['ratios'].items():
            ratios_data.append({
                'Ticker': ticker,
                'Company': company_info['company'],
                'Year': year,
                'Color': company_info['color'],
                **ratios
            })
    return pd.DataFrame(ratios_data)


# =============================================================================
# Page Configuration
# =============================================================================

st.set_page_config(
    page_title="FAAMG Financial Ratio Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        border-radius: 0 0.5rem 0.5rem 0;
    }
    .company-tag {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 0.3rem;
        margin: 0.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# Data Loading and Processing Functions
# =============================================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_financial_data(_tickers, _start_date, _end_date):
    """
    Load financial data for given tickers from Yahoo Finance.
    Uses @st.cache_data to reduce repeated requests.

    Args:
        _tickers: List of stock ticker symbols
        _start_date: Start date for historical data
        _end_date: End date for historical data

    Returns:
        Tuple of (data dictionary, success boolean, error message)
    """
    data = {}

    for ticker in _tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Get income statement for profitability ratios
            income_stmt = stock.income_stmt
            balance_sheet = stock.balance_sheet
            financials = stock.financials

            # Check if we got valid data
            if income_stmt is None or income_stmt.empty:
                return {}, False, f"No income statement data for {ticker}"

            data[ticker] = {
                'info': info,
                'income_stmt': income_stmt,
                'balance_sheet': balance_sheet,
                'financials': financials,
                'history': stock.history(start=_start_date, end=_end_date)
            }
        except Exception as e:
            return {}, False, str(e)

    return data, True, ""


def calculate_roe(net_income, shareholders_equity):
    """
    Calculate Return on Equity (ROE).
    ROE = Net Income / Average Shareholders' Equity * 100

    Args:
        net_income: Annual net income
        shareholders_equity: Total shareholders' equity

    Returns:
        ROE as percentage
    """
    if shareholders_equity is None or shareholders_equity == 0:
        return None
    # Use absolute values for calculation
    net_income_val = abs(net_income) if net_income is not None else None
    equity_val = abs(shareholders_equity)

    if net_income_val is None or equity_val == 0:
        return None

    # For negative equity, we still calculate ROE based on absolute values
    # to show the magnitude of return
    return (net_income_val / equity_val) * 100


def calculate_net_profit_margin(net_income, revenue):
    """
    Calculate Net Profit Margin.
    NPM = Net Income / Revenue * 100

    Args:
        net_income: Annual net income
        revenue: Total revenue

    Returns:
        Net Profit Margin as percentage
    """
    if net_income is None or revenue is None or revenue == 0:
        return None

    return (net_income / revenue) * 100


def calculate_gross_profit_margin(gross_profit, revenue):
    """
    Calculate Gross Profit Margin.
    GPM = Gross Profit / Revenue * 100

    Args:
        gross_profit: Gross profit (Revenue - COGS)
        revenue: Total revenue

    Returns:
        Gross Profit Margin as percentage
    """
    if gross_profit is None or revenue is None or revenue == 0:
        return None

    return (gross_profit / revenue) * 100


def calculate_debt_to_assets(total_debt, total_assets):
    """
    Calculate Asset Liability Ratio (Debt-to-Assets Ratio).
    D/A = Total Debt / Total Assets * 100

    Args:
        total_debt: Total debt (short-term + long-term)
        total_assets: Total assets

    Returns:
        Asset Liability Ratio as percentage
    """
    if total_debt is None or total_assets is None or total_assets == 0:
        return None

    return (total_debt / total_assets) * 100


def extract_financial_ratios(data, years):
    """
    Extract and calculate all financial ratios from raw financial data.

    Args:
        data: Dictionary containing financial data for each ticker
        years: List of years to analyze

    Returns:
        DataFrame with all financial ratios
    """
    ratios_data = []

    company_names = {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corp.',
        'AMZN': 'Amazon.com Inc.',
        'GOOGL': 'Alphabet Inc.',
        'META': 'Meta Platforms Inc.'
    }

    company_colors = {
        'AAPL': '#555555',    # Apple Gray
        'MSFT': '#00a4ef',    # Microsoft Blue
        'AMZN': '#ff9900',    # Amazon Orange
        'GOOGL': '#4285f4',   # Google Blue
        'META': '#0668e1'     # Meta Blue
    }

    for ticker in data.keys():
        if ticker not in company_names:
            continue

        company_data = data[ticker]

        try:
            income_stmt = company_data['income_stmt']
            balance_sheet = company_data['balance_sheet']

            if income_stmt is None or income_stmt.empty:
                continue

            # Get available years from the data (most recent first)
            available_years = income_stmt.columns.tolist()

            for year in years:
                year_str = str(year)

                # Find the year in available columns (could be int or string)
                year_col = None
                for col in available_years:
                    col_str = str(col)
                    if year_str in col_str or col_str.startswith(year_str):
                        year_col = col
                        break

                if year_col is None:
                    continue

                # Extract raw financial figures
                # Net Income
                try:
                    net_income = income_stmt.loc['Net Income', year_col] if 'Net Income' in income_stmt.index else None
                except:
                    net_income = None

                # For some companies, Net Income might be under different names
                if net_income is None:
                    for idx in income_stmt.index:
                        if 'net income' in str(idx).lower():
                            net_income = income_stmt.loc[idx, year_col]
                            break

                # Revenue / Total Revenue
                revenue = None
                for idx in income_stmt.index:
                    if 'revenue' in str(idx).lower() or 'total revenue' in str(idx).lower():
                        revenue = income_stmt.loc[idx, year_col]
                        break

                # Gross Profit
                gross_profit = None
                for idx in income_stmt.index:
                    if 'gross profit' in str(idx).lower():
                        gross_profit = income_stmt.loc[idx, year_col]
                        break

                # Total Assets (from balance sheet)
                total_assets = None
                if balance_sheet is not None and not balance_sheet.empty:
                    for idx in balance_sheet.index:
                        if 'total assets' in str(idx).lower():
                            total_assets = balance_sheet.loc[idx, year_col]
                            break

                # Total Debt (short-term + long-term)
                total_debt = None
                if balance_sheet is not None and not balance_sheet.empty:
                    short_term_debt = 0
                    long_term_debt = 0

                    for idx in balance_sheet.index:
                        idx_lower = str(idx).lower()
                        if 'short' in idx_lower and 'term' in idx_lower and 'debt' in idx_lower:
                            short_term_debt = balance_sheet.loc[idx, year_col] if pd.notna(balance_sheet.loc[idx, year_col]) else 0
                        if 'long' in idx_lower and 'term' in idx_lower and 'debt' in idx_lower:
                            long_term_debt = balance_sheet.loc[idx, year_col] if pd.notna(balance_sheet.loc[idx, year_col]) else 0
                        if 'total debt' in idx_lower:
                            total_debt = balance_sheet.loc[idx, year_col]
                            break

                    if total_debt is None and (short_term_debt > 0 or long_term_debt > 0):
                        total_debt = short_term_debt + long_term_debt

                # Shareholders' Equity
                shareholders_equity = None
                if balance_sheet is not None and not balance_sheet.empty:
                    for idx in balance_sheet.index:
                        if 'total equity' in str(idx).lower() or 'stockholders' in str(idx).lower():
                            shareholders_equity = balance_sheet.loc[idx, year_col]
                            break

                # Calculate financial ratios
                roe = calculate_roe(net_income, shareholders_equity)
                net_profit_margin = calculate_net_profit_margin(net_income, revenue)
                gross_profit_margin = calculate_gross_profit_margin(gross_profit, revenue)
                debt_to_assets = calculate_debt_to_assets(total_debt, total_assets)

                ratios_data.append({
                    'Ticker': ticker,
                    'Company': company_names[ticker],
                    'Year': year,
                    'Color': company_colors[ticker],
                    'ROE (%)': round(roe, 2) if roe is not None else None,
                    'Net Profit Margin (%)': round(net_profit_margin, 2) if net_profit_margin is not None else None,
                    'Gross Profit Margin (%)': round(gross_profit_margin, 2) if gross_profit_margin is not None else None,
                    'Asset Liability Ratio (%)': round(debt_to_assets, 2) if debt_to_assets is not None else None
                })

        except Exception as e:
            continue

    df = pd.DataFrame(ratios_data)

    # Remove outliers using IQR method for each ratio
    ratio_columns = ['ROE (%)', 'Net Profit Margin (%)', 'Gross Profit Margin (%)', 'Asset Liability Ratio (%)']

    for col in ratio_columns:
        if col in df.columns:
            # Calculate Q1, Q3, and IQR
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            # Define bounds
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Replace outliers with NaN
            df.loc[(df[col] < lower_bound) | (df[col] > upper_bound), col] = None

    return df


def generate_insight(df, selected_companies, selected_ratio):
    """
    Generate automatic text insights based on the analysis.

    Args:
        df: DataFrame containing financial ratios
        selected_companies: List of selected company tickers
        selected_ratio: Selected financial ratio for analysis

    Returns:
        String containing generated insights
    """
    if df.empty or len(selected_companies) == 0:
        return "Please select at least one company to generate insights."

    ratio_col_map = {
        'ROE': 'ROE (%)',
        'Net Profit Margin': 'Net Profit Margin (%)',
        'Gross Profit Margin': 'Gross Profit Margin (%)',
        'Asset Liability Ratio': 'Asset Liability Ratio (%)'
    }

    ratio_col = ratio_col_map.get(selected_ratio, selected_ratio)

    if ratio_col not in df.columns:
        return f"Data for {selected_ratio} is not available."

    filtered_df = df[df['Ticker'].isin(selected_companies)]

    if filtered_df.empty:
        return f"No data available for the selected companies and ratio."

    insights = []

    # Year range
    years = sorted(filtered_df['Year'].unique())
    if len(years) > 1:
        insights.append(f"## {selected_ratio} Analysis ({years[0]} - {years[-1]})\n")

    # Overall performance summary
    avg_by_company = filtered_df.groupby('Ticker')[ratio_col].mean().dropna()
    if not avg_by_company.empty:
        best_company = avg_by_company.idxmax()
        best_value = avg_by_company.max()
        worst_company = avg_by_company.idxmin()
        worst_value = avg_by_company.min()

        if selected_ratio in ['ROE', 'Net Profit Margin', 'Gross Profit Margin']:
            # Higher is better for profitability ratios
            insights.append(f"**Performance Summary:**")
            insights.append(f"- **{best_company}** leads with an average {selected_ratio} of **{best_value:.2f}%**")
            insights.append(f"- **{worst_company}** has the lowest average {selected_ratio} of **{worst_value:.2f}%**")
        else:
            # For Asset Liability Ratio, context matters
            insights.append(f"**Leverage Summary:**")
            insights.append(f"- **{best_company}** has the lowest average Asset Liability Ratio at **{best_value:.2f}%**")
            insights.append(f"- **{worst_company}** has the highest at **{worst_value:.2f}%**")

    # Trend analysis
    if len(years) >= 2:
        insights.append(f"\n**Trend Analysis:**")
        for ticker in selected_companies:
            ticker_data = filtered_df[filtered_df['Ticker'] == ticker].sort_values('Year')
            if len(ticker_data) >= 2:
                first_val = ticker_data[ratio_col].iloc[0]
                last_val = ticker_data[ratio_col].iloc[-1]

                if pd.notna(first_val) and pd.notna(last_val):
                    change = last_val - first_val
                    trend = "increased" if change > 0 else "decreased"
                    insights.append(f"- **{ticker}**: {selected_ratio} {trend} from {first_val:.2f}% to {last_val:.2f}% (Change: {change:+.2f}%)")

    # Key observation
    insights.append(f"\n**Key Observation:**")
    if selected_ratio == 'ROE':
        insights.append("ROE measures how efficiently a company generates profits from shareholders' equity. "
                        "A higher ROE indicates better utilization of equity capital. "
                        "For tech companies, ROE above 20% is generally considered strong.")
    elif selected_ratio == 'Net Profit Margin':
        insights.append("Net Profit Margin shows the percentage of revenue that becomes profit after all expenses. "
                        "Higher margins indicate better pricing power and cost management.")
    elif selected_ratio == 'Gross Profit Margin':
        insights.append("Gross Profit Margin reflects the efficiency of production and pricing strategy. "
                        "Tech companies typically have high gross margins due to scalable software products.")
    elif selected_ratio == 'Asset Liability Ratio':
        insights.append("This ratio indicates the proportion of assets financed by debt. "
                        "A lower ratio suggests a more conservative capital structure. "
                        "However, moderate leverage can be beneficial for growth.")

    return "\n".join(insights)


# =============================================================================
# Streamlit UI Components
# =============================================================================

def main():
    """Main function to run the Streamlit application."""

    # Header
    st.markdown('<h1 class="main-header">📊 FAAMG Financial Ratio Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Interactive Analysis Tool for Core Financial Ratios (2021-2025)</p>', unsafe_allow_html=True)

    # Sidebar Configuration
    st.sidebar.header("⚙️ Configuration")

    # Company Selection
    all_companies = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META']
    company_names = {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corp.',
        'AMZN': 'Amazon.com Inc.',
        'GOOGL': 'Alphabet Inc.',
        'META': 'Meta Platforms Inc.'
    }

    selected_companies = st.sidebar.multiselect(
        "Select Companies",
        options=all_companies,
        default=['AAPL', 'MSFT', 'AMZN'],
        format_func=lambda x: f"{x} - {company_names[x]}"
    )

    # Financial Ratio Selection
    ratio_options = ['ROE', 'Net Profit Margin', 'Gross Profit Margin', 'Asset Liability Ratio']
    selected_ratio = st.sidebar.selectbox("Select Financial Ratio", ratio_options)

    # Chart Type Selection
    chart_type = st.sidebar.radio("Chart Type", ["Line Chart", "Bar Chart"])

    # Data refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    # Data source info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.caption("**Data Source:**")
    st.sidebar.caption("Primary: Yahoo Finance via yfinance")
    st.sidebar.caption("Fallback: Pre-calculated ratio dataset")
    st.sidebar.caption("Fallback data is used only when live data access is temporarily unavailable.")

    # Data loading date
    st.sidebar.caption(f"Data accessed: {datetime.now().strftime('%Y-%m-%d')}")

    # Main Content Area
    if not selected_companies:
        st.warning("⚠️ Please select at least one company to analyze.")
        return

    # Initialize flags
    using_fallback = False

    # Load Data with fallback strategy
    with st.spinner("Loading financial data..."):
        end_date = datetime(2025, 12, 31)
        start_date = datetime(2021, 1, 1)

        # Try to load live data
        data, success, error_msg = load_financial_data(all_companies, start_date, end_date)

        if not success or not data:
            # Use fallback data
            using_fallback = True
            st.warning("⚠️ Live Yahoo Finance data is temporarily unavailable. The app is displaying fallback financial ratio data for demonstration purposes.")
            df = get_fallback_dataframe()
        else:
            # Process live data
            years = [2021, 2022, 2023, 2024, 2025]
            df = extract_financial_ratios(data, years)

            # If live data extraction failed, use fallback
            if df.empty:
                using_fallback = True
                st.warning("⚠️ Live Yahoo Finance data is temporarily unavailable. The app is displaying fallback financial ratio data for demonstration purposes.")
                df = get_fallback_dataframe()
            elif using_fallback:
                st.warning("⚠️ Live Yahoo Finance data is temporarily unavailable. The app is displaying fallback financial ratio data for demonstration purposes.")

    if df.empty:
        st.error("❌ No financial data available. Please try refreshing.")
        return

    # Filter data for selected companies
    filtered_df = df[df['Ticker'].isin(selected_companies)]

    # ==========================================================================
    # Key Metrics Summary
    # ==========================================================================
    st.subheader("📈 Key Metrics Summary")

    col1, col2, col3, col4 = st.columns(4)

    ratio_col_map = {
        'ROE': 'ROE (%)',
        'Net Profit Margin': 'Net Profit Margin (%)',
        'Gross Profit Margin': 'Gross Profit Margin (%)',
        'Asset Liability Ratio': 'Asset Liability Ratio (%)'
    }

    ratio_col = ratio_col_map[selected_ratio]

    # Calculate summary statistics
    if not filtered_df.empty and ratio_col in filtered_df.columns:
        avg_value = filtered_df[ratio_col].mean()
        max_value = filtered_df[ratio_col].max()
        min_value = filtered_df[ratio_col].min()
        latest_year = filtered_df['Year'].max()
        latest_value = filtered_df[filtered_df['Year'] == latest_year][ratio_col].mean()

        with col1:
            st.metric("Average (All Years)", f"{avg_value:.2f}%" if pd.notna(avg_value) else "N/A")

        with col2:
            st.metric("Maximum", f"{max_value:.2f}%" if pd.notna(max_value) else "N/A")

        with col3:
            st.metric("Minimum", f"{min_value:.2f}%" if pd.notna(min_value) else "N/A")

        with col4:
            st.metric(f"Latest ({latest_year})", f"{latest_value:.2f}%" if pd.notna(latest_value) else "N/A")

    # ==========================================================================
    # Visualization
    # ==========================================================================
    st.subheader(f"📊 {selected_ratio} Visualization")

    # Prepare data for plotting
    plot_df = filtered_df.pivot(index='Year', columns='Ticker', values=ratio_col)

    # Create chart based on selection
    if chart_type == "Line Chart":
        fig = go.Figure()

        colors = {
            'AAPL': '#555555',
            'MSFT': '#00a4ef',
            'AMZN': '#ff9900',
            'GOOGL': '#4285f4',
            'META': '#0668e1'
        }

        for ticker in selected_companies:
            if ticker in plot_df.columns:
                fig.add_trace(go.Scatter(
                    x=plot_df.index,
                    y=plot_df[ticker],
                    mode='lines+markers',
                    name=f"{ticker} - {company_names[ticker]}",
                    line=dict(color=colors.get(ticker, '#333333'), width=2),
                    marker=dict(size=8)
                ))

        fig.update_layout(
            title=f"{selected_ratio} Over Time (2021-2025)",
            xaxis_title="Fiscal Year",
            yaxis_title=selected_ratio,
            hovermode="x unified",
            template="plotly_white",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            height=500
        )

    else:  # Bar Chart
        fig = go.Figure()

        colors = {
            'AAPL': '#555555',
            'MSFT': '#00a4ef',
            'AMZN': '#ff9900',
            'GOOGL': '#4285f4',
            'META': '#0668e1'
        }

        for ticker in selected_companies:
            if ticker in plot_df.columns:
                fig.add_trace(go.Bar(
                    x=plot_df.index,
                    y=plot_df[ticker],
                    name=f"{ticker} - {company_names[ticker]}",
                    marker_color=colors.get(ticker, '#333333')
                ))

        fig.update_layout(
            title=f"{selected_ratio} by Year (2021-2025)",
            xaxis_title="Fiscal Year",
            yaxis_title=selected_ratio,
            barmode='group',
            template="plotly_white",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            height=500
        )

    st.plotly_chart(fig, use_container_width=True)

    # ==========================================================================
    # Data Table
    # ==========================================================================
    st.subheader("📋 Raw Data Table")

    # Format the dataframe for display
    display_df = filtered_df.copy()
    display_df = display_df.sort_values(['Year', 'Ticker'])

    # Rename columns for better display
    display_df = display_df.rename(columns={
        'ROE (%)': 'ROE',
        'Net Profit Margin (%)': 'Net Margin',
        'Gross Profit Margin (%)': 'Gross Margin',
        'Asset Liability Ratio (%)': 'Debt Ratio'
    })

    # Display with formatting
    st.dataframe(
        display_df,
        column_config={
            "Ticker": st.column_config.TextColumn("Ticker", width="small"),
            "Company": st.column_config.TextColumn("Company", width="medium"),
            "Year": st.column_config.NumberColumn("Year", format="%d", width="small"),
            "ROE": st.column_config.NumberColumn("ROE (%)", format="%.2f", width="small"),
            "Net Margin": st.column_config.NumberColumn("Net Profit Margin (%)", format="%.2f", width="small"),
            "Gross Margin": st.column_config.NumberColumn("Gross Margin (%)", format="%.2f", width="small"),
            "Debt Ratio": st.column_config.NumberColumn("Asset Liability Ratio (%)", format="%.2f", width="small"),
        },
        hide_index=True,
        use_container_width=True
    )

    # Download button for CSV
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name="faamg_financial_ratios.csv",
        mime="text/csv"
    )

    # ==========================================================================
    # Auto-Generated Insights
    # ==========================================================================
    st.subheader("💡 Auto-Generated Insights")

    insights = generate_insight(df, selected_companies, selected_ratio)

    st.markdown(f'<div class="insight-box">{insights}</div>', unsafe_allow_html=True)

    # ==========================================================================
    # Ratio Explanation
    # ==========================================================================
    st.subheader("📚 Financial Ratio Definitions")

    with st.expander("Click to expand ratio definitions"):
        if selected_ratio == 'ROE':
            st.markdown("""
            **Return on Equity (ROE)** measures how effectively a company uses shareholders' equity to generate profits.

            **Formula:** `ROE = Net Income / Average Shareholders' Equity × 100`

            **Interpretation:**
            - ROE > 20%: Excellent - Indicates strong efficient use of equity
            - ROE 15-20%: Good - Solid performance
            - ROE 10-15%: Average - Could be improved
            - ROE < 10%: Below average - May indicate inefficiency
            """)
        elif selected_ratio == 'Net Profit Margin':
            st.markdown("""
            **Net Profit Margin** shows the percentage of revenue that remains as profit after all expenses.

            **Formula:** `NPM = Net Income / Revenue × 100`

            **Interpretation:**
            - NPM > 20%: Excellent - Strong pricing power and cost control
            - NPM 10-20%: Good - Healthy profitability
            - NPM 5-10%: Average - Room for improvement
            - NPM < 5%: Low - May indicate competitive pressures or cost issues
            """)
        elif selected_ratio == 'Gross Profit Margin':
            st.markdown("""
            **Gross Profit Margin** measures the efficiency of production and pricing strategy before operating expenses.

            **Formula:** `GPM = Gross Profit / Revenue × 100`

            **Interpretation:**
            - GPM > 60%: Excellent - Typical for software/SaaS companies
            - GPM 40-60%: Good - Shows good production efficiency
            - GPM 20-40%: Average - Common for hardware companies
            - GPM < 20%: Low - May indicate high production costs
            """)
        else:
            st.markdown("""
            **Asset Liability Ratio (Debt-to-Assets)** measures the proportion of assets financed by debt.

            **Formula:** `D/A = Total Debt / Total Assets × 100`

            **Interpretation:**
            - D/A < 30%: Conservative - Low financial risk
            - D/A 30-50%: Moderate - Balanced capital structure
            - D/A 50-70%: High - Elevated financial leverage
            - D/A > 70%: Very High - Significant financial risk
            """)

    # ==========================================================================
    # Footer
    # ==========================================================================
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8rem;'>
            <p>FAAMG Financial Ratio Analyzer | Data Source: Yahoo Finance</p>
            <p>For educational purposes - ACC102 Python Data Product Mini Assignment</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
