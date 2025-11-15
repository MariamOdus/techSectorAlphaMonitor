# techSectorAlphaMonitor
A dynamic equity research tool that correlates "magnificent 7" stock performance with macro-economic indicators to identify investment opportunities based on fundamental valuation.

US Tech & AI Sector Investment Dashboard

🔗 Live App: Coming soon — link will be added after Streamlit Cloud deployment.

This project is an interactive equity research tool designed to replicate the workflow of a Bloomberg Intelligence (BI) Analyst.

It goes beyond simple data display by combining fundamental equity analysis (e.g., P/E ratios, ROE) with macro-economic indicators (e.g., US 10-Year Treasury Yield).
The goal: Identify which tech stocks are attractively valued — and which are overpriced — given the current economic environment.

Built entirely in Python, this tool showcases the technical and analytical skills relevant to a BI Research Associate role.

📊 Features
1. Macro Backdrop

Correlates NASDAQ-100 performance with the 10-Year Treasury Yield.

Visualizes how interest rates impact tech stock valuations.

2. Valuation Matrix

Dynamic scatter plot comparing:

P/E Ratio

YoY Revenue Growth

Instantly spot valuation outliers such as:

GARP (Growth At a Reasonable Price)

Priced for Perfection

3. Ticker Deep Dive

Select any ticker for:

Interactive candlestick chart

Key company fundamentals such as ROE, Debt-to-Equity, P/E, etc.

4. Analyst Note

Auto-generated summary research note synthesizing valuation, growth, macro sensitivity, and overall investment thesis.

🛠 Tech Stack
Category	Tools
Language	Python
Data APIs	yfinance, fredapi
Data Processing	pandas
Frontend & Charts	Streamlit, Plotly
🚀 How to Run Locally
1. Clone the repository
git clone https://github.com/YourUsername/YourRepoName.git
cd YourRepoName

2. Install dependencies
pip install -r requirements.txt

3. Run the Streamlit app
streamlit run app.py

