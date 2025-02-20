.. _zcduration:

Zero Coupon Bond Duration
=========================


In this python library we have two implementation to calculate the bond duration of a gilt zero coupon bond.

- Macaulay
- Modified Duration

For a zero-coupon bond, the Macaulay Duration is equal to the time to maturity.
Modified Duration: If the compounding frequency is not provided, the function assumes continuous compounding. For continuous compounding, the Modified Duration is equal to the time to maturity.

For discrete compounding, the Modified Duration is calculated using the formula:

.. math:: ModifiedDuration = \frac{Macaulay Duration}{(1 + \frac{r}{n})}


