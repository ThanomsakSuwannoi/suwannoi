import yfinance as yf
from datetime import datetime
import pandas as pd
from pathlib import Path
import requests
from curl_cffi.requests.exceptions import HTTPError as CurlHTTPError

# -------------------- parameters --------------------
SET50_TICKERS = [
    "ADVANC.BK",  # Advanced Info Service
    "AOT.BK",     # Airports of Thailand
    "AWC.BK",     # Asset World Corp
    "BANPU.BK",   # Banpu
    "BBL.BK",     # Bangkok Bank
    "BDMS.BK",    # Bangkok Dusit Medical Services
    "BEM.BK",     # Bangkok Expressway and Metro
    "BGRIM.BK",   # B.Grimm Power
    "BH.BK",      # Bumrungrad Hospital
    "BTS.BK",     # BTS Group Holdings
    "CBG.BK",     # Carabao Group
    "CENTEL.BK",  # Central Plaza Hotel
    "COM7.BK",    # COM7
    "CPALL.BK",   # CP ALL
    "CPF.BK",     # Charoen Pokphand Foods
    "CPN.BK",     # Central Pattana
    "CRC.BK",     # Central Retail Corporation
    "DELTA.BK",   # Delta Electronics (Thailand)
    "EA.BK",      # Energy Absolute
    "EGCO.BK",    # Electricity Generating
    "GLOBAL.BK",  # Siam Global House
    "GPSC.BK",    # Global Power Synergy
    "GULF.BK",    # Gulf Energy Development
    "HMPRO.BK",   # Home Product Center
    "IVL.BK",     # Indorama Ventures
    "KBANK.BK",   # Kasikornbank
    "KCE.BK",     # KCE Electronics
    "KTB.BK",     # Krung Thai Bank
    "KTC.BK",     # Krungthai Card
    "LH.BK",      # Land and Houses
    "MINT.BK",    # Minor International
    "MTC.BK",     # Muangthai Capital
    "OR.BK",      # PTT Oil and Retail Business
    "OSP.BK",     # Osotspa
    "PTT.BK",     # PTT
    "PTTEP.BK",   # PTT Exploration and Production
    "PTTGC.BK",   # PTT Global Chemical
    "RATCH.BK",   # Ratch Group
    "SAWAD.BK",   # Srisawad Corporation
    "SCB.BK",     # SCB X
    "SCC.BK",     # Siam Cement
    "SCGP.BK",    # SCG Packaging
    "TISCO.BK",   # Tisco Financial Group
    "TLI.BK",     # Thai Life Insurance
    "TOP.BK",     # Thai Oil
    "TRUE.BK",    # True Corporation
    "TTB.BK",     # TMBThanachart Bank
    "TU.BK",      # Thai Union Group
    "VGI.BK",     # VGI
    "WHA.BK"      # WHA Corporation
]


OUTFILE = Path(__file__).parent / "set50_stats_esg.csv"
# OUTFILE = Path("set50_stats_esg.csv")  # for testing
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
    rows = [fetch_one(t) for t in SET50_TICKERS]
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
