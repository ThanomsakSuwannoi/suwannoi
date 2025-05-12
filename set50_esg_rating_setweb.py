import re, requests, pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://setsustainability.com/libraries/1258/item/set-esg-ratings"
html = requests.get(URL, timeout=20).text
soup = BeautifulSoup(html, "html.parser")

rows = []
for tr in soup.find_all("tr"):
    cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
    if len(cells) >= 2 and cells[-1] in {"AAA","AA","A","BBB"}:
        rows.append((cells[0], cells[-1]))         # (Symbol, Rating)

df_all = pd.DataFrame(rows, columns=["Symbol", "SET_ESG_Rating"]).drop_duplicates()

SET50 = [s.replace(".BK","") for s in [
    "ADVANC.BK","AOT.BK","AWC.BK","BANPU.BK","BBL.BK","BDMS.BK","BEM.BK","BGRIM.BK",
    "BH.BK","BTS.BK","CBG.BK","CENTEL.BK","COM7.BK","CPALL.BK","CPF.BK","CPN.BK",
    "CRC.BK","DELTA.BK","EA.BK","EGCO.BK","GLOBAL.BK","GPSC.BK","GULF.BK",
    "HMPRO.BK","IVL.BK","KBANK.BK","KCE.BK","KTB.BK","KTC.BK","LH.BK","MINT.BK",
    "MTC.BK","OR.BK","OSP.BK","PTT.BK","PTTEP.BK","PTTGC.BK","RATCH.BK",
    "SAWAD.BK","SCB.BK","SCC.BK","SCGP.BK","TISCO.BK","TLI.BK","TOP.BK",
    "TRUE.BK","TTB.BK","TU.BK","VGI.BK","WHA.BK"
]]

df_set50 = (
    df_all[df_all.Symbol.isin(SET50)]
      .set_index("Symbol").reindex(SET50).reset_index()
)

out = Path(r"D:/codepython/set50_esg_ratings.csv")
df_set50.to_csv(out, index=False, encoding="utf-8-sig")
print(f"✅  Saved {len(df_set50)} rows → {out}")
