#!/usr/bin/env python3
# Simple TWStock provider using `twstock` for Taiwan stock data (示範).
# Install: pip install twstock
import os
from datetime import datetime
import pandas as pd
try:
    import twstock
except Exception:
    twstock = None

def is_twstock_available():
    return twstock is not None

def fetch_daily_twstock(stock_no: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    示範使用 twstock 抓歷史日線（twstock 有多種 fetch API，實務請根據版本調整）。
    stock_no: '2330' (純數字)
    start_date / end_date: 'YYYY-MM-DD'
    Returns: DataFrame (date, open, high, low, close, volume)
    """
    if not is_twstock_available():
        raise RuntimeError("twstock not installed. pip install twstock")
    stock = twstock.Stock(stock_no)
    records = []
    try:
        for i, p in enumerate(stock.price):
            date = stock.date[i]
            records.append({
                "date": datetime.combine(date, datetime.min.time()).date(),
                "close": p,
                "open": stock.open[i] if i < len(stock.open) else None,
                "high": stock.high[i] if i < len(stock.high) else None,
                "low": stock.low[i] if i < len(stock.low) else None,
                "volume": stock.capacity[i] if i < len(stock.capacity) else None,
            })
    except Exception:
        pass
    df = pd.DataFrame(records)
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date).date()]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date).date()]
    return df

def fetch_realtime_twstock(stock_no: str) -> dict:
    """
    回傳 twstock 提供的即時資料 (示例)。
    """
    if not is_twstock_available():
        raise RuntimeError("twstock not installed.")
    return twstock.realtime.get(stock_no)
