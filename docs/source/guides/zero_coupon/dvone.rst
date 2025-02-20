.. _zcdvone:

DV01 - Zero Coupon Bonds
=========================

In this page we cover the technical aspect of DV01 for zero coupon bonds.

DV01 Notes
^^^^^^^^^^^

The DV01 measures the change in the bond’s price due to a one-basis point (0.01%) change in yield.

The formula for DV01 can be expressed as:

.. math:

    DV01 = Modified Duration * P * 0.0001

where the Modified Duration represents

.. math:

    Modified Duration = Macaulay Duration / (1 + r / n)


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

    maturity_date = datetime.strftime(datetime.now() + timedelta(days=3650), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.01, maturity_date=maturity_date)
    print(dv01)

Which would be as calculating separately the two bonds prices and provide the difference:

.. ipython:: python
    
    from fift_analytics.gilts.zero_coupon.zc_pricers import get_zero_coupon_gilt_price
    from datetime import datetime, timedelta

    maturity_date = datetime.strftime(datetime.now() + timedelta(days=3650), "%Y-%m-%d")

    bond_price = get_zero_coupon_gilt_price(1000000, 0.01, maturity_date=maturity_date)
    print(bond_price)
    bond_price_shifted = get_zero_coupon_gilt_price(1000000, 0.0101, maturity_date=maturity_date)
    print(bond_price_shifted)
    diff = bond_price - bond_price_shifted
    print(diff)

For a zero-coupon bond with a yield of zero, the DV01 (Dollar Value of 01) would be closely related to its duration. Let’s break it down:

.. ipython:: python

    from fift_analytics.gilts.zero_coupon import calculate_zero_coupon_bond_dv01
    from fift_analytics.gilts.zero_coupon.zc_duration import calculate_zero_coupon_bond_duration    
    from datetime import datetime, timedelta

    maturity_date = datetime.strftime(datetime.now() + timedelta(days=3650), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0, maturity_date=maturity_date)
    print(dv01 / 10)
    bond_duration = calculate_zero_coupon_bond_duration(10, 0, "Modified", 2)
    print(bond_duration)

Steps:

- Calculate the bond price with the given YTM: Since the yield is 0%, the bond price will simply be the face value, which is $1,000,000.
- Calculate the bond price for a 1 basis point increase in YTM: The new YTM will be 0.0001 (0.01%).
- Calculate the DV01 as the difference between the original bond price and the new bond price:
