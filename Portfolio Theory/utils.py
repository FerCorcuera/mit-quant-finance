import argparse

import numpy as np
import pandas as pd
import requests

BASE_URL = "https://fapi.binance.com"
SYMBOL = "BTCUSDC"


def download_klines(symbol: str, start: str, end: str) -> pd.DataFrame:
    """Donload daily USD-M futures candles from binance."""

    start_ms = int(pd.Timestamp(start, tz="UTC").timestamp() * 1000)
    end_ms = int(pd.Timestamp(end, tz="UTC").timestamp() * 1000)

    response = requests.get(
        f"{BASE_URL}/fapi/v1/klines",
        params={
            "symbol": symbol,
            "interval": "1d",
            "startTime": start_ms,
            "endTime": end_ms - 1,
            "limit": 1000,
        },
        timeout=20,
    )

    response.raise_for_status()
    candles = response.json()

    if not isinstance(candles, list) or not candles:
        raise ValueError(f"No candle data returned : {candles}")

    columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_volume",
        "trades",
        "taker_buy_base",
        "taker_buy_quote",
        "ignore",
    ]

    df = pd.DataFrame(candles, columns=columns)

    df["date"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["close"] = pd.to_numeric(df["close"])

    return df[["date", "close"]].sort_values("date").reset_index(drop=True)


def calculate_log_returns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["log_return"] = np.log(result["close"] / result["close"].shift(1))

    return result.dropna().reset_index(drop=True)


def daily_index(series):
    series = series.copy()
    series.index = pd.to_datetime(series.index).tz_localize(None).normalize()
    return series.sort_index()


def main():
    parser = argparse.ArgumentParser(
        description="Download binance futures data and calculate log returns"
    )

    parser.add_argument("--symbol", default="BTCUSDC")
    parser.add_argument("--start", default="2025-01-01")
    parser.add_argument("--end", default="2026-01-01")

    args = parser.parse_args()

    previous_day = (pd.Timestamp(args.start) - pd.Timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )

    prices = download_klines(symbol=args.symbol, start=previous_day, end=args.end)

    returns = calculate_log_returns(prices)

    returns = returns[
        (returns["date"] >= args.start) & (returns["date"] < args.end)
    ].copy()

    print(returns.head())
    print(f"Number of daily returns: {len(returns)}")


if __name__ == "__main__":
    main()
