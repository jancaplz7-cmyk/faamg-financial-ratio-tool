# Reflection Report: FAAMG Financial Ratio Analysis Tool

## Analytical Problem & Target User

This project required developing an interactive data analysis tool to help Year 2 accounting, economics, and finance students, as well as beginner investors, understand FAAMG company financial performance through core ratios. The challenge was presenting complex financial data accessibly while facilitating fundamental analysis learning. The target users—students and novice investors—required an intuitive interface with educational context through auto-generated insights and plain-language interpretations.

## Dataset Description & Selection Reason

The five FAAMG companies (Apple, Microsoft, Amazon, Google, Meta) were selected because they represent well-known technology companies with diverse business models—hardware (Apple), software/services (Microsoft, Google), e-commerce (Amazon), and social media (Meta)—enabling meaningful cross-company comparisons.

The five-year period (2021-2025) captures post-pandemic recovery and recent market dynamics, including supply chain disruptions, interest rate changes, and AI-driven transformations.

Yahoo Finance via yfinance was chosen as the free, accessible data source without requiring API keys. The four core ratios—ROE, Net Profit Margin, Gross Profit Margin, and Asset Liability Ratio—were selected because they represent profitability and capital structure aspects, providing comprehensive overview without overwhelming beginners.

## Python Methods Used

Data acquisition involved using yfinance to download financial statements from Yahoo Finance, returning data in pandas DataFrames requiring careful navigation. For data cleaning, I implemented flexible string matching to handle different labeling conventions across companies. Missing values were handled through try-except blocks and availability checks before calculations.

Outlier detection using the IQR method required understanding percentile calculations and conditional logic to identify extreme values that could skew visual comparisons.

For visualization, I used matplotlib for static charts in the Jupyter notebook and Plotly for interactive Streamlit charts. The Streamlit application required learning its specific widgets, including multi-select filtering, ratio selection, and dynamic chart generation with caching decorators to optimize performance.

## Main Insights

The analysis revealed several insights. First, data quality varies significantly even among major companies—some financial metrics were reported inconsistently across years with missing values requiring careful handling.

Second, comparative analysis showed business model differences affecting ratios. Software-centric companies like Microsoft and Google tend to have higher gross margins than hardware or retail companies like Apple and Amazon.

Third, financial leverage varies considerably among successful tech companies. Some maintain conservative capital structures with low debt-to-asset ratios while others leverage more aggressively—neither approach is inherently superior as it depends on business strategy.

Finally, five-year trends showed all FAAMG companies demonstrated resilience, with most improving profitability metrics despite economic challenges. This reinforces looking at long-term trends rather than individual snapshots.

## Limitations & Improvements

Limitations include the five-year timeframe potentially missing longer-term cyclical patterns, fragile string matching for data extraction, and IQR outlier removal potentially excluding valid extreme values reflecting important business events.

Recommended improvements include adding more ratios for comprehensive analysis, implementing forecasting features, and creating benchmarking capabilities against sector averages or competitors outside tech.

## Personal Contribution & Learning

This project was my first substantial Python financial analysis application. Before this assignment, my Python skills were limited to simple scripts with cleaned academic datasets. Working with real financial data required understanding data structures, error handling, and data quality considerations.

I invested approximately 25-30 hours on this project, with most time spent on data cleaning and ensuring ratio calculations accurately reflected accounting definitions. The most challenging aspect was extracting consistent data across all five companies, each reporting information slightly differently. I also significantly improved my visualization skills—creating clear, professional charts required balancing completeness with simplicity.

## AI Use Disclosure

In completing this assignment, I used AI assistance tools for the following purposes:

1. **GitHub Copilot** (VS Code extension) - Used for code completion and suggestion refinement during Streamlit application development.

2. **ChatGPT** (OpenAI, accessed April 2026) - Used to debug yfinance extraction errors, refine Plotly configurations, improve docstrings and comments, and suggest Streamlit layout optimizations.

All AI suggestions were reviewed, tested, and modified before integration. The core analytical logic, ratio calculations, and data processing functions were implemented and verified by me to ensure accuracy and academic integrity.
