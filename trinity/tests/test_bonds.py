import typing

import pytest

import trinity.bonds as bonds
import trinity.returns as returns


class BondReturn(typing.TypedDict):
    """An expected bond return."""
    year: int
    total_return: float


@pytest.fixture
def expected_bond_returns(
    read_data: typing.Callable[[str], list[dict[str, str]]],
) -> list[BondReturn]:
    """Bond returns from the bond simulator spreadsheet."""
    rows = read_data('bonds.csv')
    return [
        BondReturn(
            year=int(row['year']),
            total_return=float(row['total_return']),
        )
        for row in rows
    ]


def test_simulate_returns(expected_bond_returns: list[BondReturn]) -> None:
    """Ensure simulated returns match published results."""
    interest_rates = [(year['rate'], year['rate_long'])
                      for year in returns.read_shiller()]

    simulated_returns = bonds.simulate_returns(interest_rates)

    for simulated, expected in zip(simulated_returns, expected_bond_returns):
        assert abs(simulated - expected['total_return']) < 0.0002
