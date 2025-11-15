# techSectorAlphaMonitor
A dynamic equity research tool that correlates "magnificent 7" stock performance with macro-economic indicators to identify investment opportunities based on fundamental valuation.

# **US Tech & AI Sector Investment Dashboard**

🔗 **Live App:** _Coming soon — link will be added after Streamlit Cloud deployment._

This project is an interactive equity research tool designed to replicate the workflow of a **Bloomberg Intelligence (BI) Analyst**.

It combines **fundamental equity analysis** (P/E ratios, ROE) with **macroeconomic indicators** (10-Year Treasury Yield) to answer:

> **"Given today’s economy, which tech stocks are undervalued — and which are simply overpriced?"**

---

## **📊 Features**

### **1. Macro Backdrop**
- Correlates **NASDAQ-100 performance** with the **10-Year Treasury Yield**
- Helps visualize the impact of interest rates on tech valuations

### **2. Valuation Matrix**
- Scatter plot comparing:
  - **Price-to-Earnings (P/E) Ratio**
  - **YoY Revenue Growth**
- Identifies:
  - *Growth At a Reasonable Price (GARP)*
  - *Priced for Perfection* stocks

### **3. Ticker Deep Dive**
- Interactive **candlestick chart**
- Key company fundamentals:
  - **ROE**
  - **Debt-to-Equity**
  - **P/E**
  - **Revenue Growth**

### **4. Analyst Note**
- Auto-generated summary research note synthesizing:
  - Valuation
  - Growth metrics
  - Macro sensitivity
  - Investment thesis

---

## **🛠 Tech Stack**

| **Category**        | **Tools**             |
|---------------------|------------------------|
| Language            | Python                 |
| Data APIs           | yfinance, fredapi      |
| Data Processing     | pandas                 |
| Frontend & Charts   | Streamlit, Plotly      |

---

## **🚀 How to Run Locally**

### **1. Clone the repository**
```bash
git clone https://github.com/YourUsername/YourRepoName.git
cd YourRepoName
```

### **2. Install dependencies**
```bash
pip install -r requirements.txt
```

### **3. Run the Streamlit app**
```bash
streamlit run app.py
```

