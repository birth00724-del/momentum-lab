import pandas as pd
import numpy as np


def calculate_momentum(price_df, lookback):
    """
    모멘텀 계산
    """
    return price_df.pct_change(lookback)


def run_backtest(
    prices,
    lookback=6,
    top_n=1,
    absolute_momentum=True,
    absolute_threshold=0,
    fee=0.00015,
    slippage=0.0005
):

    momentum = calculate_momentum(prices, lookback)

    portfolio_value = [1.0]
    dates = []
    holdings = []
    trades = []

    current_asset = None
    entry_value = 1.0
    entry_date = None

    for i in range(lookback, len(prices)-1):

        date = prices.index[i]

        current_mom = momentum.iloc[i].dropna()

        if len(current_mom) == 0:
            continue

        current_mom = current_mom.sort_values(
            ascending=False
        )

        selected = []

        for ticker in current_mom.index:

            if absolute_momentum:

                if current_mom[ticker] <= (
                    absolute_threshold / 100
                ):
                    continue

            selected.append(ticker)

            if len(selected) >= top_n:
                break

        next_returns = prices.pct_change().iloc[i+1]

        if len(selected) > 0:

            portfolio_return = (
                next_returns[selected].mean()
            )

        else:

            portfolio_return = 0

        portfolio_return -= (
            fee * 2 + slippage * 2
        )

        new_value = (
            portfolio_value[-1]
            * (1 + portfolio_return)
        )

        portfolio_value.append(new_value)

        dates.append(
            prices.index[i+1]
        )

        holding_name = (
            ",".join(selected)
            if len(selected) > 0
            else "CASH"
        )

        holdings.append(holding_name)

        if current_asset != holding_name:

            if current_asset is not None:

                trades.append({
                    "매수일": entry_date,
                    "매도일": prices.index[i+1],
                    "종목": current_asset,
                    "수익률":
                    (
                        new_value
                        / entry_value
                        - 1
                    ) * 100
                })

            current_asset = holding_name
            entry_date = prices.index[i+1]
            entry_value = new_value

    equity_curve = pd.Series(
        portfolio_value[1:],
        index=dates
    )

    holdings_df = pd.DataFrame({
        "날짜": dates,
        "보유종목": holdings
    })

    trades_df = pd.DataFrame(trades)

    return (
        equity_curve,
        holdings_df,
        trades_df
    )
