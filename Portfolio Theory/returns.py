import pandas as pd
import numpy as np


def calc_geometric_return(
    returns: pd.Series,
) -> float:
    returns = returns.dropna()
    final_growth = np.prod(1 + returns)

    return final_growth ** (1 / len(returns)) - 1


def calc_holding_period_return(
    returns: pd.Series | None = None,
    wealth: pd.Series | None = None,
) -> float:
    """
    It can receive either wealth or returns in order to calcualte the HPR"""
    if returns is not None:
        return np.prod(1 + returns) - 1

    elif wealth is not None:
        return wealth.iloc[-1] / wealth.iloc[0] - 1

    else:
        return np.nan


def calc_annualized_return(r: float, periods_per_year: float) -> float:
    return (1 + r) ** (periods_per_year) - 1


returns = pd.Series([0.15, 0.5, 0.2, -0.16, -0.2, -0.1, 0.5, 0.10])
wealth = pd.concat(
    [pd.Series([100.0]), 100 * (1 + returns).cumprod()], ignore_index=True
)

hpr = calc_holding_period_return(returns=returns)

print(calc_holding_period_return(hpr, 365))
