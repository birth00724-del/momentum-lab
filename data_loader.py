from pykrx import stock
import pandas as pd


def get_etf_name(ticker):
    """ETF 이름 조회"""
    try:
        return stock.get_etf_ticker_name(ticker)
    except:
        return ticker


def get_monthly_prices(ticker, start_date, end_date):
    """
    ETF 일봉을 받아 월말 종가로 변환
    """

    df = stock.get_etf_ohlcv_by_date(
        start_date.replace("-", ""),
        end_date.replace("-", ""),
        ticker
    )

    if df.empty:
        return pd.DataFrame()

    df = df[['종가']].copy()
    df.index = pd.to_datetime(df.index)

    monthly = df.resample('M').last()

    monthly.columns = ['Close']

    return monthly
