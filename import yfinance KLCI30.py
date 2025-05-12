import yfinance as yf
from datetime import datetime
import pandas as pd
from pathlib import Path
import requests
from curl_cffi.requests.exceptions import HTTPError as CurlHTTPError

# -------------------- parameters --------------------
KLCI_TICKERS = [
    "1155.KL",  # Malayan Banking Berhad (Maybank)
    "1023.KL",  # CIMB Group Holdings Berhad
    "1295.KL",  # Public Bank Berhad
    "5347.KL",  # Tenaga Nasional Berhad
    "5225.KL",  # IHH Healthcare Berhad
    "5819.KL",  # Hong Leong Bank Berhad
    "1082.KL",  # Hong Leong Financial Group Berhad
    "1066.KL",  # RHB Bank Berhad
    "6888.KL",  # Axiata Group Berhad
    "6947.KL",  # CelcomDigi Berhad
    "6012.KL",  # Maxis Berhad
    "4863.KL",  # Telekom Malaysia Berhad
    "6742.KL",  # YTL Power International Berhad
    "4677.KL",  # YTL Corporation Berhad
    "4065.KL",  # PPB Group Berhad
    "4707.KL",  # Nestlé (Malaysia) Berhad
    "5183.KL",  # Petronas Chemicals Group Berhad
    "5681.KL",  # Petronas Dagangan Berhad
    "6033.KL",  # Petronas Gas Berhad
    "8869.KL",  # Press Metal Aluminium Holdings Berhad
    "3816.KL",  # MISC Berhad
    "1961.KL",  # IOI Corporation Berhad
    "2445.KL",  # Kuala Lumpur Kepong Berhad
    "5285.KL",  # SD Guthrie Berhad (formerly Sime Darby Plantation)
    "4197.KL",  # Sime Darby Berhad
    "5211.KL",  # Sunway Berhad
    "5398.KL",  # Gamuda Berhad
    "5326.KL",  # 99 Speed Mart Retail Holdings Berhad
    "5296.KL",  # MR DIY Group (M) Berhad
    "7084.KL",  # QL Resources Berhad
]


OUTFILE = Path(__file__).parent / "KLCI30_stats_esg.csv"
# OUTFILE = Path("KLCI30_stats_esg.csv")  # for testing
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
    """Valuation + ESG for <tkr>; ESG handled gracefully if unavailable."""
    t    = yf.Ticker(tkr)
    info = t.info or {}

    data = {
        "Stock"            : tkr,
        "MarketCap"        : info.get("marketCap"),
        "EnterpriseVal"    : info.get("enterpriseValue"),
        "TrailingPE"       : info.get("trailingPE"),
        "ForwardPE"        : info.get("forwardPE"),
        "Beta"             : info.get("beta"),
        "DividendYield"    : info.get("dividendYield"),
        "Price/Sales"      : info.get("priceToSalesTrailing12Months"),
        "Price/Book"       : info.get("priceToBook"),
        "EV/Revenue"       : info.get("enterpriseToRevenue"),
        "EV/EBITDA"        : info.get("enterpriseToEbitda")
    }

    # —— ESG ——
    try:
        esg = t.sustainability   # may throw HTTPError from requests or curl_cffi
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
    rows = [fetch_one(t) for t in KLCI_TICKERS]
    df   = pd.DataFrame(rows)

    try:
        df.to_csv(OUTFILE, index=False, encoding="utf-8-sig")
        print(f"Saved {len(rows)} rows to {OUTFILE} on {TODAY:%d-%b-%Y}")
    except OSError as e:
        print(f"[Error] Could not write to {OUTFILE}: {e}")
        # fallback to current working directory
        fallback = Path.cwd() / OUTFILE.name
        df.to_csv(fallback, index=False, encoding="utf-8-sig")
        print(f"Saved instead to {fallback} on {TODAY:%d-%b-%Y}")
