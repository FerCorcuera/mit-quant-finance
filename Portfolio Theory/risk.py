r = 0.15
sdv = 0.3

risk_free_rate = 0.02

A = 4


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


answer = mean_variance_utility(r, A, sdv, True, risk_free_rate)

print(
    f"Utility: {answer[0]:.2%} vs {risk_free_rate:.2%}, \n and the critical risk adversion is: {answer[1]}"
)
