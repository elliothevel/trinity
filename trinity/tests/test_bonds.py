import trinity.bonds as bonds
import trinity.returns as returns


def test_simulate_returns(expected_bond_returns):
    """Ensure simulated returns match published results."""
    interest_rates = [(year['rate'], year['rate_long'])
                      for year in returns.read_shiller()]

    simulated_returns = bonds.simulate_returns(interest_rates)

    for simulated, expected in zip(simulated_returns, expected_bond_returns):
        assert abs(simulated - expected['total_return']) < 0.0002
