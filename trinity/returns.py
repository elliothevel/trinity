"""Tools for calculating historical market returns."""
import csv
import io
import pkgutil

import trinity.bonds as bonds


def get_returns():
    """Calculate historic market returns.

    Based on Shiller's annual long term stock, bond, interest
    rate and consumption data, which can be found at
    http://www.econ.yale.edu/~shiller/data.htm

    Returns
    -------
    dict
        Keys are years and values are dictionaries with the
        keys "stocks" and "bonds". Each value represents
        an inflation-adjusted annual return.
    """
    shiller = read_shiller()
    bond_returns = get_bond_returns(shiller)
    returns = {}
    for current, future in zip(shiller[:-1], shiller[1:]):
        year = current['year']
        returns[year] = annual_returns(current, future, bond_returns[year])
    return returns


def annual_returns(current, future, bond_return):
    """Calculate returns from successive years of Shiller data.

    Parameters
    ----------
    current, future : dict
        Shiller data for the current year and the next year.
    bond_return : float
        Simulated nominal bond return for the current year.

    Returns
    -------
    dict
        Real stock and bond returns for this year.
    """
    inflation = future['cpi'] / current['cpi'] - 1

    stock_return = real_return(
        ((future['price']
          + current['dividends']
          - current['price']) / current['price']), inflation)
    bond_return = real_return(bond_return, inflation)

    return {'stocks': stock_return, 'bonds': bond_return}


def real_return(nominal_return, inflation_rate):
    """Calculate an inflation-adjusted return.

    Parameters
    ----------
    nominal_return : float
        Nominal return.
    inflation_rate : float
        Inflation rate.

    Returns
    -------
    float
        Real (inflation-adjusted) return.
    """
    return (1 + nominal_return) / (1 + inflation_rate) - 1


def get_bond_returns(shiller):
    """Get simulated bond returns by year.

    Parameters
    ----------
    shiller : list of dict
        Raw data from the Shiller data set.

    Returns
    -------
    dict
        Nominal bond returns by year.
    """
    years, interest_rates = zip(
        *[(row['year'],
           (row['rate'], row['rate_long']))
          for row in shiller]
    )
    bond_returns = bonds.simulate_returns(interest_rates)
    return dict(zip(years, bond_returns))


def read_shiller():
    """Read raw data from the Shiller data set.

    Returns
    -------
    list of dict
        Market data by year.
    """
    raw = pkgutil.get_data(__name__, 'data/shiller.csv')
    buf = io.StringIO(raw.decode())
    reader = csv.DictReader(buf)
    return [{'year': int(row['YEAR']),
             'price': float(row['P']),
             'dividends': float(row['D']),
             'rate': float(row['R']) / 100.0,
             'rate_long': float(row['RLONG']) / 100.0,
             'cpi': float(row['CPI'])}
            for row in reader]
