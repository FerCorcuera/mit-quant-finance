from scipy.stats import norm
import numpy as np
import math
import random
import matplotlib.pyplot as plt


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


def geometric_return(
    returns: np.ndarray,
) -> float:
    final_growth = np.prod(1 + returns)

    geometric_return = final_growth ** (1 / len(returns)) - 1

    return geometric_return


def scenario_analysis(
    probabilities: np.ndarray,
    future_prices: np.ndarray,
    purchase_price: double,
    cash_payments: double,
    risk_free_rate: double,
    initial_investment: double,
):
    """
    We are assumming constant cash paymetns across all scenarios
    """
    hpr = (future_prices + cash_payments - purchase_price) / purchase_price
    expected_return = np.dot(probabilities, hpr, out=None)
    deviations = hpr - expected_return
    squared_deviations = deviations**2
    variance_hpr = np.dot(probabilities, squared_deviations)
    risk = np.sqrt(variance_hpr)
    risk_premium = expected_return - risk_free_rate
    expected_value = initial_investment * (1 + expected_return)

    results = {
        "HPR": hpr,
        "Expected_return": expected_return,
        "Variance_HPR": variance_hpr,
        "Risk": risk,
        "Risk_premium": risk_premium,
        "Expected_value": expected_value,
    }

    return results


def value_at_risk(
    exposure: float,
    alpha: float,
    expected_return: float,
    volatility: float,
) -> tuple[float, float]:
    """We calculate the value at risk under normal distribution assumption
    It returns:
    - q: the lower -tail return quantile
    - var: the corresponding monetary var given the exposure
    """

    q = norm.ppf(
        alpha,
        loc=expected_return,
        scale=volatility,
    )

    var = exposure * (-q)

    return (q, var)


def lower_partial_standard_deviation(
    returns: np.ndarray,
    target_return: float,
) -> float:
    shortfalls = np.minimum(returns - target_return, 0)
    return np.sqrt(np.mean(shortfalls**2))


def sortino_ratio(
    returns: np.ndarray,
    target_return: float,
) -> float:
    expected_excess_return = np.mean(returns) - target_return

    downside_risk = lower_partial_standard_deviation(
        returns,
        target_return,
    )

    return expected_excess_return / downside_risk


def negative_three_sigma_frequency(
    returns: np.ndarray,
) -> [float, float, float]:
    mean = np.mean(returns)
    volatility = np.std(returns, ddof=1)  # for samples and not population metrics

    threshold = mean - 3 * volatility

    empirical_freq = np.mean(returns <= threshold)

    normal_freq = norm.cdf(-3)

    return threshold, empirical_freq, normal_freq


class ZeroCouponBond:
    def __init__(self, price, maturity, face_value, compounding_freq):
        """
        express the maturity in year relative terms, examplae:

        - 1 Year: 1
        - 0.5 years : 0.5
        - 25 years : 25

        """

        self.price = price
        self.maturity = maturity
        self.face_value = face_value
        self.r = face_value / price - 1
        self.compounding_freq = compounding_freq

        print(
            f"This a bond with price {self.price}, maturity of {self.maturity} and return of {self.r:.2%}"
        )

    def get_effective_anual_rate(self):
        ear = (1 + self.r) ** (1 / self.maturity) - 1

        return ear

    def get_annual_percentage_rate(self):
        ear = self.get_effective_anual_rate()

        apr = ((1 + ear) ** (1 / self.compounding_freq) - 1) * self.compounding_freq

        return apr

    def get_continuous_compounding_rate(self):
        ear = self.get_effective_anual_rate()
        r_cc = math.log(1 + ear)

        return r_cc

    def get_real_growth(self, inflation_rate):
        """
        Please introduce the inflation of the for the same maturity
        """

        real_growth = (1 + self.r) / (1 + inflation_rate) - 1

        real_face_value = self.price * (1 + real_growth)
        return (real_growth, real_face_value)

    def get_after_tax_rate(self, inflation_rate, tax_rate):
        """
        Returns a tuple with the real_rate after tax and the returned value
        """

        real_after_tax_rate = (1 + self.r * (1 - tax_rate)) / (1 + inflation_rate) - 1
        real_after_tax_value = self.price * (1 + real_after_tax_rate)
        return (real_after_tax_rate, real_after_tax_value)


# annual_returns = np.array([0.2869,0.1088,0.0491])
# risk_free_rate = 0.06
#
# arimetic_avg = np.mean(annual_returns)
# geometric_avg = geometric_return(annual_returns)
# squared_devs = ( annual_returns - arimetic_avg ) ** 2
# sdv = np.std(annual_returns, ddof = 1)
# corrected_sdv = np.sqrt( squared_devs.sum()/(len(squared_devs) -1 ) )
# sharp_ratio = ( arimetic_avg - risk_free_rate )/sdv
# corrected_sharpe_ratio = ( arimetic_avg - risk_free_rate)/corrected_sdv
#
# print(f"arimetic average return: {arimetic_avg:.2%}")
#
# print(f"geometric average return: {geometric_avg:.2%}")
# print(f"Standard dev: {sdv:.2%}")
# print(f" Corrected standard deviation: {corrected_sdv:.2%}")
# print(f"Shapre Ratio: {sharp_ratio:.2%} vs Corrected sharpe_ratio: {corrected_sharpe_ratio:.2%}")
