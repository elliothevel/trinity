import pytest

import trinity
import trinity.simulation as simulation


def test_main(script_runner):
    """Ensure simulations can be run from the main entrypoint."""
    ret = script_runner.run(
        'trinity',
        '--stock-allocation', '0.75',
        '--years', '20',
        '--withdrawal-rate', '0.04',
        '--start-year', '1926',
        '--end-year', '1995'
    )
    assert ret.success
    assert ret.stdout == '1.0\n'
    assert ret.stderr == ''


def test_calc_success_rate(expected_outcomes):
    """Ensure simulations align with published results."""
    end_year, cases = expected_outcomes
    returns = trinity.get_returns(1926, end_year)
    error = 0.0
    for case in cases:
        success_rate = simulation.calc_success_rate(
            returns,
            case['stock_allocation'],
            case['years'],
            case['withdrawal_rate'])
        error += abs(success_rate - case['success_rate'])

    # Because of differences in data sources, especially in
    # the type of bonds, we are unable to replicate published
    # results exactly. Here we assert that the mean average
    # error is less than some reasonable threshold.
    # When run against the same Ibbotson data used in the
    # original study, the mean average error is ~0.001.
    mae = error / len(cases)
    assert mae < 0.03


@pytest.mark.parametrize('duration,expected', [
    # These numbers are given in tables 1 and 3 in
    # the original study.
    (15, 56),
    (20, 51),
    (25, 46),
    (30, 41),
])
def test_get_periods(duration, expected):
    """Ensure correct year ranges are calculated."""
    periods = simulation.get_periods(1926, 1995, duration)
    assert len(periods) == expected
