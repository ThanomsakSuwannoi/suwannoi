from playwright.sync_api import sync_playwright
import pandas as pd, re
from pathlib import Path

SET50_SYMBOLS = [s.replace(".BK", "") for s in [
    "ADVANC.BK","AOT.BK","AWC.BK","BANPU.BK","BBL.BK","BDMS.BK","BEM.BK",
    "BGRIM.BK","BH.BK","BTS.BK","CBG.BK","CENTEL.BK","COM7.BK","CPALL.BK",
    "CPF.BK","CPN.BK","CRC.BK","DELTA.BK","EA.BK","EGCO.BK","GLOBAL.BK",
    "GPSC.BK","GULF.BK","HMPRO.BK","IVL.BK","KBANK.BK","KCE.BK","KTB.BK",
    "KTC.BK","LH.BK","MINT.BK","MTC.BK","OR.BK","OSP.BK","PTT.BK",
    "PTTEP.BK","PTTGC.BK","RATCH.BK","SAWAD.BK","SCB.BK","SCC.BK",
    "SCGP.BK","TISCO.BK","TLI.BK","TOP.BK","TRUE.BK","TTB.BK","TU.BK",
    "VGI.BK","WHA.BK"
]]

def scrape_live_ratings(url: str = "https://setsustainability.com/libraries/1258/item/set-esg-ratings"):
    """Return a DataFrame [Symbol, SET_ESG_Rating] scraped via Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page    = browser.new_page()
        # give the page plenty of time; network can be slow
        page.goto(url, timeout=60_000)

        # wait until any rating bucket appears in text
        page.wait_for_selector("text=/AAA|AA|A|BBB/", timeout=60_000)
        html = page.content()
        browser.close()

    # regex-extract lines like  “ADVANC … AAA”
    pattern = re.compile(r"\b([A-Z]{2,6})\b.*?\b(AAA|AA|A|BBB)\b")
    records = pattern.findall(html)

    if not records:
        raise RuntimeError("No Symbol/Rating pairs found – check page or regex.")

    return (
        pd.DataFrame(records, columns=["Symbol", "SET_ESG_Rating"])
          .drop_duplicates()
          .sort_values("Symbol", ignore_index=True)
    )

def main():
    df_all   = scrape_live_ratings()
    df_set50 = (
        df_all[df_all["Symbol"].isin(SET50_SYMBOLS)]
          .set_index("Symbol")
          .reindex(SET50_SYMBOLS)         # preserve official order
          .reset_index()
    )

    out_path = Path(r"D:/codepython/set50_esg_ratings.csv")
    df_set50.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"✅  Saved {len(df_set50)} rows → {out_path}")

if __name__ == "__main__":
    main()

