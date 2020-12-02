## Trinity

A simple retirement calculator based on the Trinity study
[[1]](#1).

This tool attempts to reproduce results published in the Trinity
study using only freely available data.

### Background

The Trinity study analyzes how historical portfolio success
rates are affected by stock/bond allocation, length of
retirement period, and withdrawal rate.

Given a retirement period in years, it finds all historical
periods of the same duration. A simulation is run for each
period using actual market returns and inflation-adjusted
withdrawals. The portfolio's success rate is then the number
of simulations for which the portfolio survived divided by
the number of periods.

### Data

The original Trinity study used S&P 500 and long-term corporate bond
returns from Ibbotson.
Unfortunately, the Ibbotson data is not freely available.
This program uses data from
[Robert Shiller's website](http://www.econ.yale.edu/~shiller/data.htm)
instead.

The Shiller data set includes annual S&P 500 prices, 1-year
and 10-year interest rates, and CPI data.
To calculate bond returns from interest rates, a bond fund simulation
is run. This approach is described in
[this thread](https://www.bogleheads.org/forum/viewtopic.php?t=179425)
on Bogleheads.org.

Given the differences in bond return data, numbers produced by
this program tend to differ more from published results as length
of retirement period and bond allocation increase.

### Usage

#### Command line
```
$ trinity \
$   --stock-allocation 0.75 \
$   --years 20 \
$   --withdrawal-rate 0.04
1.0
```
Use `trinity --help` for more documentation.

#### Library
```
>>> import trinity
>>> returns = trinity.get_returns()
>>> trinity.calc_success_rate(returns, 0.75, 20, 0.04)
1.0
```

### Development

Install the package and dev dependencies
```
$ python setup.py develop
$ pip install -r dev-requirements.txt
```

Run the tests
```
$ ./test.sh
```

### References

<a id="1">[1]</a>
Cooley, Philip L.; Hubbard, Carl M.; Walz, Daniel T. (1998).
Retirement Savings: Choosing a Withdrawal Rate That Is Sustainable.
AAII Journal, 10 (3): 16–21.
