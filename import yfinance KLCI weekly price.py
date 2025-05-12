import yfinance as yf
import pandas as pd

# --- your existing KLCI_TICKERS list here ---
KLCI_TICKERS = [
    "1155.KL", "1023.KL", "1295.KL", "5347.KL", "5225.KL", "5819.KL",
    "1082.KL", "1066.KL", "6888.KL", "6947.KL", "6012.KL", "4863.KL",
    "6742.KL", "4677.KL", "4065.KL", "4707.KL", "5183.KL", "5681.KL",
    "6033.KL", "8869.KL", "3816.KL", "1961.KL", "2445.KL", "5285.KL",
    "4197.KL", "5211.KL", "5398.KL", "5326.KL", "5296.KL", "7084.KL"
]

# 1️⃣  Download 3 years of *weekly* OHLCV
raw = yf.download(
    KLCI_TICKERS,
    group_by="ticker",
    period="3y",
    interval="1wk",   # <-- weekly bars
    auto_adjust=False # set True if you want splits/dividends adjusted
)

# 2️⃣  Keep only the Close field for every ticker
#     With group_by="ticker", the DataFrame has a two-level column index:
#     level 0 = ticker, level 1 = field (Open, High, Low, Close, Volume)
weekly_close = raw.xs("Close", axis=1, level=1)

# 3️⃣  Persist to CSV
weekly_close.to_csv("klci_weekly_close.csv")
print("Saved weekly closing prices to klci_weekly_close.csv")
