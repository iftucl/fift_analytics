.. _zcdvone:

DV01 - Zero Coupon Bonds
=========================

In this page we cover the technical aspect of DV01 for zero coupon bonds.

DV01 Notes
^^^^^^^^^^^

The DV01 measures the change in the bond’s price due to a one-basis point (0.01%) change in yield.

The formula for DV01 can be expressed as:

.. math:: DV01 = Modified Duration * P * 0.0001

where the Modified Duration represents

.. math:: ModifiedDuration = \frac{Macaulay Duration}{(1 + \frac{r}{n})}


DV01 implementation
^^^^^^^^^^^^^^^^^^^^

To use the ``fift_analytics.gilts.zero_coupon`` implementation, you can import it as:

.. ipython:: python
    :okexcept:

    from fift_analytics.gilts.zero_coupon import calculate_zero_coupon_bond_dv01

This implementation relies on the ``fift_analytics.gilts.zero_coupon`` function ``get_zero_coupon_gilt_price``.

This implementation will compute first the zero coupon bond price using the provided yield to maturity and maturity date and then recomputes the zero coupon bond price using same maturity date but shifting the yield up by one basis point.

Suppose you want to calculate the DV01 for a zero coupon gilt at face value of 1 Million GBP with a yield to maturity of 1% and maturity date in 10 years time:

.. ipython:: python

    from fift_analytics.gilts.zero_coupon import calculate_zero_coupon_bond_dv01
    from datetime import datetime, timedelta

    maturity_date = datetime.strftime(datetime.now() + timedelta(days=365), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.01, maturity_date=maturity_date, n_decimals=2)
    print(f"DV01 of the zero-coupon bond: ${dv01:.2f}")

Which would be as to calculate the two bonds prices and provide the difference:

.. ipython:: python
    
    from fift_analytics.gilts.zero_coupon.zc_pricers import get_zero_coupon_gilt_price

    bond_price = get_zero_coupon_gilt_price(1000000, 0.01, maturity_date=maturity_date)
    print(f"The bond price is: ${bond_price:.2f}")
    bond_price_shifted = get_zero_coupon_gilt_price(1000000, 0.0101, maturity_date=maturity_date)
    print(f"The shifted bond price is: ${bond_price_shifted:.2f}")
    diff = bond_price - bond_price_shifted
    print(f"DV01 of the zero-coupon bond: ${diff:.2f}")

For a zero-coupon bond with a yield of zero, the DV01 (Dollar Value of 01) would be closely related to its duration. Let’s break it down:

.. ipython:: python

    from fift_analytics.gilts.zero_coupon import calculate_zero_coupon_bond_dv01
    from fift_analytics.gilts.zero_coupon.zc_duration import calculate_zero_coupon_bond_duration    

    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0, maturity_date=maturity_date)
    print(f"DV01 of the zero-coupon bond: ${dv01:.2f}")
    
    bond_duration = calculate_zero_coupon_bond_duration(1, 0, "Modified", 2)
    bond_price = get_zero_coupon_gilt_price(1000000, 0.01, maturity_date=maturity_date)
    approx_dv01 = bond_duration * bond_price * 0.0001
    print(f"Approximation DV01 of the zero-coupon bond: ${approx_dv01:.2f}")

Steps:

- Calculate the bond price with the given YTM: Since the yield is 0%, the bond price will simply be the face value, which is $1,000,000.
- Calculate the bond price for a 1 basis point increase in YTM: The new YTM will be 0.0001 (0.01%).
- Calculate the DV01 as the difference between the original bond price and the new bond price:
