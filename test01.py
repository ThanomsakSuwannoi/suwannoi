import yfinance as yf
import pandas as pd
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

data = yf.download(KLCI_TICKERS, group_by="ticker", period="3y", interval="1d")
data.to_csv("klci_price_history.csv")
print("Saved 3-year daily OHLCV for all KLCI names.")
