import yfinance as yf
from datetime import datetime
import pandas as pd
from pathlib import Path
import requests

# -------------------- parameters --------------------
STI_TICKERS = [
    "D05.SI","O39.SI","U11.SI","S68.SI","9CI.SI","C38U.SI","A17U.SI","J69U.SI",
    "BUOU.SI","ME8U.SI","M44U.SI","N2IU.SI","C09.SI","U14.SI","H78.SI","BN4.SI",
    "U96.SI","S63.SI","5E2.SI","BS6.SI","C6L.SI","S58.SI","Z74.SI","D01.SI",
    "C07.SI","J36.SI","G13.SI","Y92.SI","F34.SI","V03.SI"
]

OUTFILE = Path(r"C:\Users\Thanomsak Suwannoi\Downloads\codepython\sti_stats_esg.csv")
TODAY   = datetime.now()

# -------------------- helpers --------------------
def _grab_esg(df, metric):
    """Return the value of <metric> regardless of dataframe layout."""
    if df is None or df.empty:
        return None
    if metric in df.index:
        row = df.loc[metric]
        return row["Value"] if "Value" in row else row.iloc[0]
    if metric in df.columns:
        return df[metric].iloc[0]
    return None


def fetch_one(tkr):
    """Valuation + ESG for <tkr>; ESG handled gracefully if unavailable."""
    t   = yf.Ticker(tkr)
    inf = t.info or {}

    data = {
        "Stock"        : tkr,
        "MarketCap"    : inf.get("marketCap"),
        "EnterpriseVal": inf.get("enterpriseValue"),
        "TrailingPE"   : inf.get("trailingPE"),
        "ForwardPE"    : inf.get("forwardPE"),
        "PEG_5yr"      : inf.get("pegRatio"),                  # NEW
        "Beta"         : inf.get("beta"),                      # NEW
        "DividendYield": inf.get("dividendYield"),             # NEW (decimal, e.g., 0.038 ➜ 3.8 %)
        "Price/Sales"  : inf.get("priceToSalesTrailing12Months"),
        "Price/Book"   : inf.get("priceToBook"),
        "EV/Revenue"   : inf.get("enterpriseToRevenue"),
        "EV/EBITDA"    : inf.get("enterpriseToEbitda")
    }

    # ---------- ESG (wrapped in try/except) ----------
    try:
        esg = t.sustainability           # triggers the quoteSummary call
    except requests.exceptions.HTTPError:
        esg = None                       # e.g. 404 – no ESG coverage

    data.update({
        "ESG_Total"        : _grab_esg(esg, "totalEsg"),
        "ESG_Environmental": _grab_esg(esg, "environmentScore"),
        "ESG_Social"       : _grab_esg(esg, "socialScore"),
        "ESG_Governance"   : _grab_esg(esg, "governanceScore"),
        "ControversyLevel" : _grab_esg(esg, "highestControversy")
    })

    return data

# -------------------- run --------------------
rows = [fetch_one(t) for t in STI_TICKERS]
pd.DataFrame(rows).to_csv(OUTFILE, index=False, encoding="utf-8-sig")
print(f"Saved {len(rows)} rows to {OUTFILE} on {TODAY:%d-%b-%Y}")
