import yfinance as yf
from datetime import datetime
import pandas as pd
from pathlib import Path
import requests
from curl_cffi.requests.exceptions import HTTPError as CurlHTTPError

# -------------------- parameters --------------------
STI_TICKERS = [
    "D05.SI","O39.SI","U11.SI","S68.SI","9CI.SI","C38U.SI","A17U.SI","J69U.SI",
    "BUOU.SI","ME8U.SI","M44U.SI","N2IU.SI","C09.SI","U14.SI","H78.SI","BN4.SI",
    "U96.SI","S63.SI","5E2.SI","BS6.SI","C6L.SI","S58.SI","Z74.SI","D01.SI",
    "C07.SI","J36.SI","G13.SI","Y92.SI","F34.SI","V03.SI"
]

OUTFILE = Path(__file__).parent / "sti_stats_esg.csv"

TODAY   = datetime.now()

# -------------------- helpers --------------------
def _grab_esg(df, metric):
    """Return the value of <metric> regardless of dataframe layout."""
    if df is None or df.empty:
        return None
    if metric in df.index:
        row = df.loc[metric]
        return row.get("Value", row.iloc[0])
    if metric in df.columns:
        return df[metric].iloc[0]
    return None

def fetch_one(tkr):
    """Fetch valuation + ESG for <tkr>; ESG errors are caught gracefully."""
    t   = yf.Ticker(tkr)
    info = t.info or {}

    data = {
        "Stock"            : tkr,
        "MarketCap"        : info.get("marketCap"),
        "EnterpriseVal"    : info.get("enterpriseValue"),
        "TrailingPE"       : info.get("trailingPE"),
        "ForwardPE"        : info.get("forwardPE"),
        "PEG_5yr"          : info.get("pegRatio"),
        "Beta"             : info.get("beta"),
        "DividendYield"    : info.get("dividendYield"),
        "Price/Sales"      : info.get("priceToSalesTrailing12Months"),
        "Price/Book"       : info.get("priceToBook"),
        "EV/Revenue"       : info.get("enterpriseToRevenue"),
        "EV/EBITDA"        : info.get("enterpriseToEbitda")
    }

    # —— ESG ——
    try:
        esg = t.sustainability   # may raise HTTPError from requests or curl_cffi
    except (requests.exceptions.HTTPError, CurlHTTPError) as e:
        print(f"[Warning] No ESG for {tkr}: {e}")
        esg = None
    except Exception as e:
        print(f"[Error] Unexpected ESG error for {tkr}: {e}")
        esg = None

    data.update({
        "ESG_Total"        : _grab_esg(esg, "totalEsg"),
        "ESG_Environmental": _grab_esg(esg, "environmentScore"),
        "ESG_Social"       : _grab_esg(esg, "socialScore"),
        "ESG_Governance"   : _grab_esg(esg, "governanceScore"),
        "ControversyLevel" : _grab_esg(esg, "highestControversy")
    })

    return data

# -------------------- run --------------------
if __name__ == "__main__":
    rows = [fetch_one(t) for t in STI_TICKERS]
    df   = pd.DataFrame(rows)
    df.to_csv(OUTFILE, index=False, encoding="utf-8-sig")
    print(f"Saved {len(rows)} rows to {OUTFILE} on {TODAY:%d-%b-%Y}")
