"""Bond fund simulation."""
import collections


def simulate_returns(rates):
    """Simulate total returns of a bond fund.

    Follows the approach described in
    https://www.bogleheads.org/forum/viewtopic.php?t=179425

    The fund contains ten bonds with 2-10 years until maturity.
    Each year the bond with one year until maturity is sold at
    the current 1-year interest rate and a new bond is purchased
    at the current 10-year rate. Annual returns are calculated
    by summing the present value of all bonds in the fund, using
    linear interpolation to estimate 2-9 year interest rates.

    Parameters
    ----------
    rates : iterable of tuple
        Set of 1-year and 10-year interest rates by year.

    Returns
    -------
    list of float
        Total returns for each year in `rates`.
    """
    rates = iter(rates)

    ladder = collections.deque(maxlen=10)
    rate, rate_long = next(rates)
    init_ladder(ladder, rate_long)
    nav = calc_nav(ladder, rate, rate_long)

    returns = []
    for rate, rate_long in rates:
        step(ladder, rate_long)
        tmp = calc_nav(ladder, rate, rate_long)
        total_return = round(tmp / nav - 1, 4)
        returns.append(total_return)
        nav = tmp

    return returns


def step(ladder, rate_long):
    """Advance the bond ladder by one year.

    Sells the bond in the ladder with one year left until
    maturity and buys a new 10-year bond at the current
    interest rate.

    Parameters
    ----------
    ladder : collections.deque
        A bond ladder.
    rate_long : float
        Current 10-year interest rate.
    """
    # Sum payments received this year.
    capital = sum(rate*par for rate, par in ladder)

    # Sell bond with one year left until maturity.
    par, _ = ladder.popleft()
    capital += par

    # Purchase new bond at current 10-year rate.
    ladder.append((capital, rate_long))


def calc_nav(ladder, rate, rate_long):
    """Calculate the net asset value of a fund.

    Parameters
    ----------
    ladder : collections.deque
        A bond ladder.
    rate : float
        Current 1-year interest rate.
    rate_long : float
        Current 10-year interest rate.

    Returns
    -------
    float
        Approximate value of the assets in `ladder`.
    """
    nav = 0.0
    for i, (par, bond_rate) in enumerate(ladder, 1):
        current_rate = calc_rate(rate, rate_long, i)
        nav -= pv(current_rate, i, par*bond_rate, par)
    return nav


def init_ladder(ladder, rate):
    """Initialize a bond ladder.

    The ladder is bootstrapped by buying 10 bonds
    at the initial interest rate. The par value of
    the oldest bond is set to $1. Par values of the
    remaining bonds are set to $1 plus any coupon
    payments from older bonds.

    Parameters
    ----------
    ladder : collections.deque
        Empty bond ladder.
    rate : float
        Initial 10-year rate.
    """
    for n in range(10):
        par = (1 + rate)**n
        ladder.append((par, rate))


def calc_rate(rate, rate_long, maturity):
    """Approximate a current interest rate.

    Permforms linear interpolation based on the current
    1-year and 10-year rates and the maturity of the
    bond.

    Parameters
    ----------
    rate : float
        1-year interest rate.
    rate_long : float
        10-year interest rate.
    maturity : int
        Maturity of the bond in years.

    Returns
    -------
    float
        Approximated interest rate.
    """
    return rate + (rate_long - rate)*(maturity - 1) / 9


def pv(rate, nper, pmt, fv):
    """Calculate the present value of an asset.

    Parameters
    ----------
    rate : float
        Interest rate per period.
    nper : int
        Number of payment periods.
    pmt : float
        Constant payment made each period.
    fv : float
        Future value, i.e., balance after the last
        payment is made.

    Returns
    -------
    float
    """
    if rate == 0:
        return -(fv + pmt*nper)
    else:
        tmp = (1 + rate)**nper
        return -(fv + pmt*(tmp - 1) / rate) / tmp
