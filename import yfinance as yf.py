import yfinance as yf
from datetime import datetime
import pandas as pd

# Update to use the current date
target_date = datetime.now()

# Fetch data for multiple stocks and export to CSV
stocks = [
    "D05.SI",  # DBS Group Holdings Ltd
    "O39.SI",  # Oversea-Chinese Banking Corporation (OCBC)
    "U11.SI",  # United Overseas Bank (UOB)
    "S68.SI",  # Singapore Exchange (SGX)
    "9CI.SI",  # CapitaLand Investment Ltd
    "C38U.SI",  # CapitaLand Integrated Commercial Trust
    "A17U.SI",  # CapitaLand Ascendas REIT
    "J69U.SI",  # Frasers Centrepoint Trust
    "BUOU.SI",  # Frasers Logistics & Commercial Trust
    "ME8U.SI",  # Mapletree Industrial Trust
    "M44U.SI",  # Mapletree Logistics Trust
    "N2IU.SI",  # Mapletree Pan Asia Commercial Trust
    "C09.SI",  # City Developments Ltd
    "U14.SI",  # UOL Group Ltd
    "H78.SI",  # Hongkong Land Holdings Ltd
    "BN4.SI",  # Keppel Corporation Ltd
    "U96.SI",  # Sembcorp Industries Ltd
    "S63.SI",  # Singapore Technologies Engineering Ltd (ST Engineering)
    "5E2.SI",  # Seatrium Ltd (formerly Sembcorp Marine)
    "BS6.SI",  # Yangzijiang Shipbuilding Holdings Ltd
    "C6L.SI",  # Singapore Airlines Ltd (SIA)
    "S58.SI",  # SATS Ltd
    "Z74.SI",  # Singapore Telecommunications Ltd (Singtel)
    "D01.SI",  # DFI Retail Group Holdings Ltd
    "C07.SI",  # Jardine Cycle & Carriage Ltd
    "J36.SI",  # Jardine Matheson Holdings Ltd
    "G13.SI",  # Genting Singapore Ltd
    "Y92.SI",  # Thai Beverage Public Co Ltd
    "F34.SI",  # Wilmar International Ltd
    "V03.SI"   # Venture Corporation Ltd
]

# Remove ESG rating and add available statistics from Yahoo Finance
market_caps = []

# Add a warning log for missing PEG ratio
for stock in stocks:
    ticker = yf.Ticker(stock)
    historical_data = ticker.history(period="1d")  # Fetch the latest available data
    if not historical_data.empty:
        market_cap = ticker.info.get("marketCap", "Market Cap not available")
        enterprise_value = ticker.info.get("enterpriseValue", "Enterprise Value not available")
        trailing_pe = ticker.info.get("trailingPE", "Trailing P/E not available")
        forward_pe = ticker.info.get("forwardPE", "Forward P/E not available")
        price_to_sales = ticker.info.get("priceToSalesTrailing12Months", "Price/Sales not available")
        price_to_book = ticker.info.get("priceToBook", "Price/Book not available")
        ev_to_revenue = ticker.info.get("enterpriseToRevenue", "Enterprise Value/Revenue not available")
        ev_to_ebitda = ticker.info.get("enterpriseToEbitda", "Enterprise Value/EBITDA not available")
    else:
        market_cap = "No data available"
        enterprise_value = "No data available"
        trailing_pe = "No data available"
        forward_pe = "No data available"
        price_to_sales = "No data available"
        price_to_book = "No data available"
        ev_to_revenue = "No data available"
        ev_to_ebitda = "No data available"

    # Remove PEG Ratio column from the output
    market_caps.append({
        "Stock": stock,
        "Market Capitalization": market_cap,
        "Enterprise Value": enterprise_value,
        "Trailing P/E": trailing_pe,
        "Forward P/E": forward_pe,
        "Price/Sales": price_to_sales,
        "Price/Book": price_to_book,
        "Enterprise Value/Revenue": ev_to_revenue,
        "Enterprise Value/EBITDA": ev_to_ebitda
    })

# Convert to DataFrame and export to CSV
df_market_caps = pd.DataFrame(market_caps)
output_file = "c:/Users/Thanomsak Suwannoi/Downloads/codepython/market_statistics.csv"
df_market_caps.to_csv(output_file, index=False)

print(f"Market capitalization and statistics data for {target_date.strftime('%d %B %Y')} exported to: {output_file}")