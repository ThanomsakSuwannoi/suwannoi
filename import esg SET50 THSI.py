# ---------------------------------------------------------
# SET50  ➜  SET ESG Rating  (Excel-download method, 2025)
# ---------------------------------------------------------
import io
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

# ----- 1)  Your SET50 tickers (.BK stripped) -------------
SET50_TICKERS = [
    "ADVANC.BK","AOT.BK","AWC.BK","BANPU.BK","BBL.BK","BDMS.BK","BEM.BK",
    "BGRIM.BK","BH.BK","BTS.BK","CBG.BK","CENTEL.BK","COM7.BK","CPALL.BK",
    "CPF.BK","CPN.BK","CRC.BK","DELTA.BK","EA.BK","EGCO.BK","GLOBAL.BK",
    "GPSC.BK","GULF.BK","HMPRO.BK","IVL.BK","KBANK.BK","KCE.BK","KTB.BK",
    "KTC.BK","LH.BK","MINT.BK","MTC.BK","OR.BK","OSP.BK","PTT.BK",
    "PTTEP.BK","PTTGC.BK","RATCH.BK","SAWAD.BK","SCB.BK","SCC.BK",
    "SCGP.BK","TISCO.BK","TLI.BK","TOP.BK","TRUE.BK","TTB.BK","TU.BK",
    "VGI.BK","WHA.BK"
]
SET50_SYMBOLS = [t.replace(".BK", "") for t in SET50_TICKERS]

# ----- 2)  Find the live Excel link on the sustainability page -------------
BASE_URL  = "https://setsustainability.com"
ARTICLE   = "/libraries/1258/item/set-esg-ratings"

html = requests.get(BASE_URL + ARTICLE, timeout=20).text
soup = BeautifulSoup(html, "html.parser")

xlsx_href = None
for a in soup.find_all("a", href=True):
    if a["href"].lower().endswith(".xlsx"):
        xlsx_href = a["href"]
        break

if not xlsx_href:
    raise RuntimeError("⚠️  Could not locate an .xlsx link on the ESG ratings page.")

xlsx_url = xlsx_href if xlsx_href.startswith("http") else BASE_URL + xlsx_href
print(f"Downloading Excel file: {xlsx_url}")

# ----- 3)  Download Excel into memory & read with pandas -------------------
xlsx_bytes = requests.get(xlsx_url, timeout=30).content
raw_df = pd.read_excel(io.BytesIO(xlsx_bytes), sheet_name=0)

# The Excel file typically has Thai headers; find columns by pattern matching
symbol_col, rating_col = None, None
for col in raw_df.columns:
    if re.search(r"(?i)symbol|ticker|ชื่อย่อ", col):
        symbol_col = col
    if re.search(r"(?i)rating|เรทติ้ง|ระดับ", col):
        rating_col = col
if not symbol_col or not rating_col:
    raise RuntimeError("⚠️  Could not identify Symbol or Rating columns in the Excel file.")

raw_df = raw_df[[symbol_col, rating_col]].rename(
    columns={symbol_col: "Symbol", rating_col: "SET_ESG_Rating"}
)

# ----- 4)  Filter to SET50, keep original order ---------------------------
df_set50 = (
    raw_df[raw_df["Symbol"].isin(SET50_SYMBOLS)]
      .set_index("Symbol")
      .reindex(SET50_SYMBOLS)          # maintain SET50 order
      .reset_index()
)

# ----- 5)  Save to CSV -----------------------------------------------------
out_path = Path(r"D:/codepython/set50_esg_ratings.csv")
df_set50.to_csv(out_path, index=False, encoding="utf-8-sig")
print(f"✅  Saved {len(df_set50)} rows to {out_path}")
