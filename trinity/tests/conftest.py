import csv
import os

import pytest


DATA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'data')


@pytest.fixture
def expected_outcomes():
    """Success rates published in the original study."""
    filepath = os.path.join(DATA_DIR, 'outcomes.csv')
    with open(filepath) as fp:
        reader = csv.DictReader(fp)
        return [{'stock_allocation': float(row['stock_allocation']),
                 'years': int(row['years']),
                 'withdrawal_rate': float(row['withdrawal_rate']),
                 'success_rate': float(row['success_rate'])}
                for row in reader]


@pytest.fixture
def expected_bond_returns():
    """Bond returns from the bond simulator spreadsheet."""
    filepath = os.path.join(DATA_DIR, 'bonds.csv')
    with open(filepath) as fp:
        reader = csv.DictReader(fp)
        return [{'year': int(row['year']),
                 'total_return': float(row['total_return'])}
                for row in reader]
