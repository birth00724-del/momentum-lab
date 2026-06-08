import numpy as np


def calculate_cagr(equity_curve):

    if len(equity_curve) < 2:
        return 0

    years = (
        (equity_curve.index[-1]
         - equity_curve.index[0]).days
        / 365.25
    )

    if years <= 0:
        return 0

    cagr = (
        (equity_curve.iloc[-1]
         / equity_curve.iloc[0])
        ** (1 / years)
        - 1
    )

    return cagr * 100


def calculate_mdd(equity_curve):

    running_max = equity_curve.cummax()

    drawdown = (
        equity_curve
        / running_max
        - 1
    )

    mdd = drawdown.min()

    return mdd * 100


def calculate_total_return(
    equity_curve
):

    total_return = (
        equity_curve.iloc[-1]
        / equity_curve.iloc[0]
        - 1
    )

    return total_return * 100


def calculate_metrics(
    equity_curve
):

    return {
        "CAGR":
            round(
                calculate_cagr(
                    equity_curve
                ),
                2
            ),

        "MDD":
            round(
                calculate_mdd(
                    equity_curve
                ),
                2
            ),

        "총수익률":
            round(
                calculate_total_return(
                    equity_curve
                ),
                2
            )
    }
