import pandas as pd
import numpy as np

from risk import (
    calc_expected_shortfall,
    calc_maximum_drawdown,
    calc_value_at_risk,
    calc_lower_partial_sdv,
    calc_sharpe_ratio,
    calc_sortino_ratio,
    calc_sigma_tail_frequency,
)


from returns import (
    calc_geometric_return,
    calc_holding_period_return,
    calc_annualized_return,
)


def perfomance_metrics(
    wealth: pd.Series,
    returns: pd.Series,
    risk_free_rate: pd.Series,
    periods_per_year: 252,
    target_return: float = 0.0,
) -> dict[str, float]:
    # Valuation metrics
    initial_value = wealth.iloc[0]
    final_value = wealth.iloc[-1]

    returns_mean = returns.mean()
    returns_std = returns.std()

    # return metrics

    hpr = calc_holding_period_return(returns=returns)
    geometric_mean = calc_geometric_return(returns=returns)

    # risk metrics

    max_drawdown = calc_maximum_drawdown(wealth)
    var95 = calc_value_at_risk(
        returns, alpha=0.05, exposure=final_value, parametric=True
    )

    nonp_var95 = calc_value_at_risk(
        returns, alpha=0.05, exposure=final_value, parametric=False
    )

    var99 = calc_value_at_risk(
        returns, alpha=0.01, exposure=final_value, parametric=True
    )

    nonp_var99 = calc_value_at_risk(
        returns, alpha=0.01, exposure=final_value, parametric=False
    )

    expected_shortfall = calc_expected_shortfall(
        returns,
        target_return,
    )

    excess_return = returns - risk_free_rate
    period_mean_excess_returns = excess_return.mean()
    period_std_excess_returns = excess_return.std()
    period_sharpe_ratio = calc_sharpe_ratio(returns, risk_free_rate)

    lower_parital_sdv = calc_lower_partial_sdv(
        returns,
        target_return,
    )

    sortino_ratio = calc_sortino_ratio(returns, target_return)

    sigma_tail_frequency = calc_sigma_tail_frequency(returns=returns)

    return {
        "Initial_value": initial_value,
        "Final_value": final_value,
        "Holding_period_return": hpr,
        "Arimetic_mean": returns_mean,
        "Geometric_mean": geometric_mean,
        "Annualized_aritmetic_mean": calc_annualized_return(returns_mean),
        "Daily_volatiliy": returns_std,
        "Annualized_volatility": returns_std * np.sqrt(periods_per_year),
        "Worst_period_return": returns.min(),
        "Max_drawdown": max_drawdown,
        "Parametric_VaR95": var95,
        "Non_Parametric_Var95": nonp_var95,
        "Parametric_VaR99": var99,
        "Non_Parametric_Var99": nonp_var99,
        "Expected_shortfall": expected_shortfall,
        "Period_mean_excess_returns": period_mean_excess_returns,
        "Period_std_excess_returns": period_std_excess_returns,
        "Period_sharpe_ratio": period_sharpe_ratio,
        "Annualzied_sharpe_ratio": period_sharpe_ratio * np.sqrt(periods_per_year),
        "Lower_partial_sdv": lower_parital_sdv,
        "Sortino_ratio": sortino_ratio,
        "Sigma_tail_frequency": sigma_tail_frequency,
    }
