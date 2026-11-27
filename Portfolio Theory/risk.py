import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm


def plot_return_distribution(returns: np.ndarray, title: str, compare: bool = False):
    returns = np.asarray(returns, dtype=float)
    returns = returns[np.isfinite(returns)]

    mu = np.mean(returns)
    sigma = np.std(returns, ddof=1)

    x = np.linspace(returns.min(), returns.max(), 500)

    plt.figure(figsize=(10, 5))

    plt.hist(
        returns,
        bins=40,
        density=True,
        alpha=0.6,
        label="Empirical returns",
    )

    if compare:
        plt.plot(
            x, norm.pdf(x, loc=mu, scale=sigma), label="Fitted normal distribution"
        )

    plt.title(title)
    plt.xlabel("Return")
    plt.ylabel("Proability Density")
    plt.legend()
    plt.show()


def calc_maximum_drawdown(
    wealth: pd.Series,
) -> float:
    """
    Given a pandas time series this function calculates
    the maximum drawndown.
    It represents the biggest peak-to-through drop over the period
    """

    running_max = wealth.cummax()
    drawdown = wealth / running_max - 1

    return drawdown.min()


def calc_value_at_risk(
    returns: pd.Series,
    alpha: float = 0.01,
    exposure: float = 100,
    parametric: bool = False,
) -> tuple[float, float]:
    """
    Calculates the value at risk of a given pandas series.
    It can calculate parametric VaR that assumes normal distribution
    But by default it calcualtes non parametric VaR, that returns a quantile and the loss
    Parameters:
    - returns: the returns series (as a pandas series)
    - alpha: at what level would be calculated the VaR, default by 0.01
    - exposure: to calculate the loss, default by 100
    - parametric: default by False
    """
    if parametric:
        mean = returns.mean()
        std = returns.std()
        q = norm.ppf(alpha, loc=mean, scale=std)

        return (q, exposure * -q)
    q = returns.quantile(alpha)
    return (q, exposure * -q)


def calc_expected_shortfall(
    returns: pd.Series,
    threshold: float,
) -> float:
    """
    Simple expected shortfall function,
    given a pandas series and a threshold calculates the mean return on the interval below the threshold
    """

    expected_shortfall = returns[returns <= threshold].mean()

    return expected_shortfall


def calc_lower_partial_sdv(
    returns: pd.Series,
    target_return: float,
) -> float:
    """
    Calcualtes the standard deviation including as zero all the points over the specifiec return,
    Isolates the "bad" volatility on the left tail of return weighting it with thier frequency
    """
    shortfalls = np.minimum(returns - target_return, 0)
    return np.sqrt(np.mean(shortfalls**2))


def calc_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: pd.Series,
) -> float:
    """
    Assumes that both series observation are in the same time interval
    If one has more periods than the other, only the observations that share same date in both series will be accounted for the calculation
    """

    excess_return = (returns - risk_free_rate).dropna()
    mean = excess_return.mean()
    std = excess_return.std()

    if std == 0:
        return np.nan

    return mean / std


def calc_sortino_ratio(
    returns: pd.Series,
    target_return: float,
) -> float:
    expected_excess_return = returns.mean() - target_return

    downside_risk = calc_lower_partial_sdv(
        returns,
        target_return,
    )

    return expected_excess_return / downside_risk


def calc_sigma_tail_frequency(
    returns: pd.Series,
) -> tuple[float, float, float]:
    mean = returns.mean()
    volatility = returns.std()

    threshold = mean - 3 * volatility

    empirical_freq = np.mean(returns <= threshold)
    normal_freq = norm.cdf(-3)

    return (threshold, empirical_freq, empirical_freq / normal_freq)


def mean_variance_utility(
    expected_return: float,
    adverse_parameter: float,
    sigma: float,
    solve_A: bool = False,
    risk_free_rate=0,
) -> float:
    """Calculate mean-vairance ulity (certainty equivalent)"""

    u = expected_return - 0.5 * (adverse_parameter * sigma**2)

    if solve_A:
        optimal_A = ((expected_return - risk_free_rate) * 2) / sigma**2

        return (u, optimal_A)

    return u


returns = pd.Series([0.15, 0.5, 0.2, -0.16, -0.2, -0.1, 0.5, 0.10])
var = calc_value_at_risk(returns)

print(var)
