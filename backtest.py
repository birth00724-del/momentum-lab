import pandas as pd
import numpy as np


def calculate_momentum(prices, lookback):
    return prices.pct_change(lookback)


def run_backtest(
    prices,
    lookback=6,
    top_n=1,
    absolute_momentum=True,
    absolute_threshold=0,
    fee=0.00015,
    slippage=0.0005
):

    momentum = calculate_momentum(
        prices,
        lookback
    )

    portfolio_value = 1.0

    equity_curve = []
    holdings_log = []
    rebalance_log = []
    trades = []

    current_holding = None
    entry_date = None
    entry_value = None

    portfolio_dates = []

    monthly_returns = prices.pct_change()

    for i in range(lookback, len(prices) - 1):

        current_date = prices.index[i]

        mom = momentum.iloc[i].dropna()

        if len(mom) == 0:
            continue

        mom = mom.sort_values(
            ascending=False
        )

        ranking = []

        for ticker in mom.index:

            ranking.append(
                (
                    ticker,
                    mom[ticker]
                )
            )

        selected = []

        for ticker in mom.index:

            if absolute_momentum:

                if mom[ticker] <= (
                    absolute_threshold / 100
                ):
                    continue

            selected.append(ticker)

            if len(selected) >= top_n:
                break

        next_date = prices.index[i + 1]

        if len(selected) > 0:

            portfolio_return = (
                monthly_returns.loc[
                    next_date,
                    selected
                ].mean()
            )

            holding_text = ",".join(
                selected
            )

        else:

            portfolio_return = 0

            holding_text = "CASH"

        portfolio_return -= (
            fee * 2
            + slippage * 2
        )

        portfolio_value *= (
            1 + portfolio_return
        )

        equity_curve.append(
            portfolio_value
        )

        portfolio_dates.append(
            next_date
        )

        holdings_log.append(
            {
                "날짜": next_date,
                "보유종목": holding_text
            }
        )

        rebalance_log.append(
            {
                "날짜": current_date,
                "순위": ranking[:10],
                "선택종목": holding_text
            }
        )

        if current_holding != holding_text:

            if current_holding is not None:

                trade_return = (
                    portfolio_value
                    / entry_value
                    - 1
                ) * 100

                trades.append(
                    {
                        "매수일": entry_date,
                        "매도일": next_date,
                        "종목": current_holding,
                        "수익률(%)":
                            round(
                                trade_return,
                                2
                            )
                    }
                )

            current_holding = holding_text

            entry_date = next_date

            entry_value = portfolio_value

    equity_curve = pd.Series(
        equity_curve,
        index=portfolio_dates
    )

    holdings_df = pd.DataFrame(
        holdings_log
    )

    rebalance_df = pd.DataFrame(
        rebalance_log
    )

    trades_df = pd.DataFrame(
        trades
    )

    return {
        "equity_curve":
            equity_curve,

        "holdings":
            holdings_df,

        "rebalance":
            rebalance_df,

        "trades":
            trades_df
    }
