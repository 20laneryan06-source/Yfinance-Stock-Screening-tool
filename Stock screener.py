#Created for freshman year project in UTSA Investment society Student portfolio
#simple program returning key chartersitics used

import yfinance as yf
import pandas as pd


print("Screener functions: fetch_stock, build_screener, format_market_cap")

# yfinance key -> column name shown in the table
FIELDS = {
    "currentPrice": "Price",
    "marketCap": "Market Cap",
    "sector": "Sector",
    "trailingPE": "P/E Ratio",
    "fiftyTwoWeekHigh": "52W High",
    "fiftyTwoWeekLow": "52W Low",
}


def fetch_stock(ticker):
    #Return a dict of screener fields for one ticker.
    try:
        info = yf.Ticker(ticker).info
    except Exception as e:
        print(f"Could not fetch {ticker}: {e}")
        return None

    row = {"Ticker": ticker.upper()}
    for key, label in FIELDS.items():
        row[label] = info.get(key)  # None if missing (e.g. no P/E for unprofitable firms)
    return row


def build_screener(tickers):
    rows = [r for r in (fetch_stock(t) for t in tickers) if r]
    return pd.DataFrame(rows)


def format_market_cap(value):
    if value is None or pd.isna(value):
        return "N/A"
    for threshold, suffix in [(1e12, "T"), (1e9, "B"), (1e6, "M")]:
        if value >= threshold:
            return f"{value / threshold:.2f}{suffix}"
    return str(value)


def main():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "XOM", "NVDA"]

    df = build_screener(tickers)

    # ---- Optional filters (comment out or change as you like) ----
    # df = df[df["P/E Ratio"] < 30]                 # P/E under 30
    # df = df[df["Sector"] == "Technology"]         # only tech stocks
    # df = df[df["Market Cap"] > 100e9]             # market cap over $100B

    # Sort by market cap, largest first
    df = df.sort_values("Market Cap", ascending=False)

    # Make the output easier to read
    df["Market Cap"] = df["Market Cap"].apply(format_market_cap)
    df["P/E Ratio"] = df["P/E Ratio"].round(2)

    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
