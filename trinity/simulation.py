"""Tools for simulating retirement outcomes."""
import argparse

from trinity.returns import get_returns


def main():
    """Simulate historical portfolio success rates."""
    parser = argparse.ArgumentParser(description='Retirement calculator')
    parser.add_argument(
        '-s', '--stock-allocation',
        type=float,
        required=True,
        help='Fraction of the portfolio invested in equities.')
    parser.add_argument(
        '-y', '--years',
        type=int,
        required=True,
        help='Length of retirement period.')
    parser.add_argument(
        '-w', '--withdrawal-rate',
        type=float,
        required=True,
        help='Withdrawal rate as a fraction of initial portfolio size.')
    args = parser.parse_args()

    returns = get_returns()
    success_rate = calc_success_rate(
        returns,
        args.stock_allocation, args.years, args.withdrawal_rate)

    print(success_rate)


def calc_success_rate(returns, stock_allocation, duration, withdrawal_rate):
    """Calculate an historical portfolio success rate.

    Parameters
    ----------
    returns : dict
        Historical stock and bond returns by year.
        Keys are the years and values are dicts with the
        keys "stocks" and "bonds".
    stock_allocation : float
        Fraction of the portfolio allocated to equities.
    duration : int
        Length of withdrawal period in years.
    withdrawal_rate : float
        Annual withdrawal rate as a fraction of the initial
        portfolio size.

    Returns
    -------
    float
        The fraction of periods for which the portfolio
        survived, rounded to two decimal places.
    """
    # The trinity study is limited to 1926 to 1995.
    periods = get_periods(1926, 1995, duration)
    successes = sum(
        simulate(returns, *period, stock_allocation, withdrawal_rate)
        for period in periods
    )
    success_rate = successes / len(periods)
    return round(success_rate, 2)


def simulate(returns, start_year, end_year, stock_allocation, withdrawal_rate):
    """Simulate portfolio performance.

    Parameters
    ----------
    returns : dict
        Historical stock and bond returns by year.
    start_year, end_year : int
        Simulate performance between these years.
    stock_allocation : float
        Fraction of the portfolio allocated to equities.
    withdrawal_rate : float
        Annual withdrawal rate as a fraction of the initial
        portfolio size.

    Returns
    -------
    success : bool
        Whether the portfolio survived.
    """
    # Simulations are independent of initial portfolio size,
    # so use a fixed, realistic number.
    balance = 1_000_000
    withdrawal = balance * withdrawal_rate

    for year in range(start_year, end_year + 1):
        balance = update_portfolio(
            returns[year], withdrawal, stock_allocation, balance)

    return balance > 0


def update_portfolio(returns, withdrawal, stock_allocation, balance):
    """Update a portfolio based on performance in a single year.

    Parameters
    ----------
    returns : dict
        Stock and bond returns for a single year.
    withdrawal : float
        Amount to withdraw from the portfolio. The withdrawal
        is assumed to take place at the end of the year after
        adjusting for inflation.
    stock_allocation : float
        The fraction of the portfolio to allocate to equities.
        The update calculations assume the portfolio is rebalanced
        annually.
    balance : float
        Portfolio balance at the beginning of the year.

    Returns
    -------
    balance : float
        The balance at the and of the year after accounting for
        all market gains and withdrawals.
    """
    return (
        # stocks plus appreciation and dividends
        balance * stock_allocation * (1 + returns['stocks'])
        # bonds plus bond income
        + balance * (1 - stock_allocation) * (1 + returns['bonds'])
        # end of year withdrawal
        - withdrawal
    )


def get_periods(start_year, end_year, duration):
    """Get periods over which to simulate returns.

    Find all continuous periods of `duration` years that
    fall completely between the given start and end years.

    Parameters
    ----------
    start_year, end_year : int
        Starting and ending years.
    duration : int
        Return periods of this many years.

    Returns
    -------
    list of tuple
        List of (start year, end year) pairs.
    """
    periods = []
    year = start_year
    while year + duration - 1 <= end_year:
        periods.append((year, year + duration - 1))
        year += 1
    return periods
