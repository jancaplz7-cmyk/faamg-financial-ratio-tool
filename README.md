# FAAMG Tech Stocks Financial Ratio Analysis Tool

## Project Title
**FAAMG Core Financial Ratios Interactive Analysis Tool**

---

## Problem & User

### Problem Definition
This project addresses the challenge faced by Year 2 accounting, economics, and finance students, as well as beginner investors, in understanding and comparing the financial performance of major technology companies. The FAAMG stocks (Apple, Microsoft, Amazon, Google, Meta) are among the most influential companies in the global market, yet their financial metrics can be complex and overwhelming for those new to fundamental analysis.

### Target Users
- Year 2 accounting/economics/finance students learning financial statement analysis
- Beginner investors seeking to understand fundamental analysis concepts
- Educators teaching financial ratio analysis with real-world examples

---

## Data Source

### Primary Data Source
- **Yahoo Finance** via `yfinance` Python library
- **Access Date:** April 2026
- **Data Type:** Financial statements (Income Statement, Balance Sheet)

### Target Companies
| Ticker | Company Name |
|--------|--------------|
| AAPL | Apple Inc. |
| MSFT | Microsoft Corporation |
| AMZN | Amazon.com Inc. |
| GOOGL | Alphabet Inc. |
| META | Meta Platforms Inc. |

### Time Range
- **Analysis Period:** 2021-2025 (5 fiscal years)

---

## Methods

### Financial Ratios Calculated

1. **Return on Equity (ROE)**
   - Formula: `Net Income / Average Shareholders' Equity × 100`
   - Interpretation: Measures efficiency in generating profits from shareholders' capital

2. **Net Profit Margin (NPM)**
   - Formula: `Net Income / Revenue × 100`
   - Interpretation: Shows percentage of revenue remaining as profit after all expenses

3. **Gross Profit Margin (GPM)**
   - Formula: `Gross Profit / Revenue × 100`
   - Interpretation: Indicates production efficiency before operating costs

4. **Asset Liability Ratio (Debt-to-Assets)**
   - Formula: `Total Debt / Total Assets × 100`
   - Interpretation: Measures financial leverage and capital structure

### Data Processing Methods
- **Missing Value Handling:** Identification and reporting of missing data points
- **Outlier Removal:** IQR (Interquartile Range) method
  - Outliers defined as values outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
- **Time Unification:** Standardized fiscal year formatting

### Visualization Tools
- **Matplotlib:** Static line charts and bar charts
- **Plotly:** Interactive charts with hover functionality

---

## Key Findings

### ROE (Return on Equity)
- Companies with consistently high ROE demonstrate efficient utilization of shareholder equity
- Tech companies generally show ROE above 20%, indicating strong performance

### Net Profit Margin
- Software-oriented companies (Microsoft, Google) typically show higher net margins
- Retail-oriented companies (Amazon) may show lower margins due to different business models

### Gross Profit Margin
- All FAAMG companies maintain healthy gross margins above 40%
- Software/SaaS products exhibit higher gross margins than physical products

### Asset Liability Ratio
- Conservative capital structure varies by company growth strategy
- Lower ratios indicate more equity-financed operations

### 5-Year Trends
- Most companies showed recovery and growth post-2021
- Margin improvements visible across the technology sector
- Financial leverage became more conservative after 2022

---

## How to Run

### Local Installation

1. **Clone or download the repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the application:**
   - Open your browser and navigate to `http://localhost:8501`

### Using the Jupyter Notebook

1. **Open the notebook:**
   ```bash
   jupyter notebook ACC102_Track4_FAAMG_Financial_Analysis.ipynb
   ```

2. **Run cells sequentially** from the notebook menu (Kernel → Restart & Run All)

### Deployment to Streamlit Community Cloud

1. Push all files to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Deploy

---

## Product Link

**Streamlit Application:** Deployed on Streamlit Community Cloud
- Main file: `app.py`
- Features interactive company comparison, ratio selection, and auto-generated insights

---

## Limitations & Next Steps

### Current Limitations
1. **Data Range:** Limited to 5 fiscal years (2021-2025)
2. **Missing Values:** Some financial metrics may have gaps due to differences in reporting across companies
3. **Outlier Handling:** IQR method may exclude valid extreme values
4. **Historical Focus:** Ratios are historical and may not predict future performance
5. **Single Sector:** Analysis limited to technology/communication services sector

### Recommended Next Steps
1. **Expand Coverage:** Add more companies for broader market comparison
2. **Additional Ratios:** Include P/E ratio, EPS, Current Ratio, Quick Ratio
3. **Forecasting:** Implement time-series forecasting for trend prediction
4. **Industry Benchmarks:** Add sector average comparisons
5. **Real-time Updates:** Implement automatic data refresh functionality
6. **Export Features:** Add PDF report generation capability

---

## Project Structure

```
├── app.py                              # Streamlit interactive application
├── ACC102_Track4_FAAMG_Financial_Analysis.ipynb  # Jupyter notebook with full analysis
├── README.md                           # This documentation
├── Reflection_Report.md                # Personal reflection report
├── Demo_Video_Script.md                # Demo video narration script
└── requirements.txt                    # Python dependencies
```

---

## Academic Information

- **Course:** ACC102 Python Data Product Mini Assignment
- **Track:** 4 (Interactive Python Tool + Streamlit App - Bonus Track)
- **Topic:** FAAMG Tech Stocks Core Financial Ratios Interactive Analysis Tool
- **Submission Date:** April 2026

---

## Disclaimer

This analysis is for **educational purposes only** and should not be considered financial advice. Always conduct thorough research and consult with qualified financial advisors before making investment decisions.
