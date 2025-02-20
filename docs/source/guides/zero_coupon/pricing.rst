.. _zcpricing:

Pricing - Zero Coupon Bonds
============================

In this page we cover the technical aspect of the pricing for zero coupon bonds.


The main public API to revaluate the price of a bond price can be imported from `fift_analytics` as:

.. ipython:: python
    :okexcept:

    from fift_analytics.gilts.zero_coupon import get_zero_coupon_gilt_price


get_zero_coupon_gilt_price
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Input Parameters:

- Face Value :math:`( F )`: The maturity value of the bond.
- Annual Yield :math:`( r )`: The annual yield to maturity as a decimal (e.g., 0.04 for 4%).
- Maturity Date: The date when the bond matures.
- Settlement Date: The date when the bond is settled (defaults to today if not provided).



Calculate Time to Maturity:

Calculate the number of days between the settlement date and the maturity date.
Convert this to years using the Actual/Actual (ISMA) day count convention.

.. math:: Time to Maturity = \frac{\text{Days to Maturity}}{\text{Year Length}}

Where:

.. math::
    
    \text{Days to Maturity} = \text{Maturity Date} - \text{Settlement Date}
    \text{Year Length} = 365 \text{ or } 366 \text{ (depending on leap year)}

Compute Price Using Continuous Compounding:

Use the continuous compounding formula to calculate the bond price.

.. math::
    P = F \cdot e^{-r \cdot t}
    
Where:

:math:`( P )` is the present price of the bond.
:math:`( F )` is the face value of the bond.
:math:`( r )` is the annual yield to maturity.
:math:`( t )` is the time to maturity in years.

.. ipython:: python
    :okexcept:
    
    import math

    face_value = 100
    annual_yield = 0.03
    time_to_maturity = 0.5
    
    present_value = face_value * math.exp(-annual_yield * time_to_maturity)
    print(round(present_value, 2))

Handle Edge Cases
^^^^^^^^^^^^^^^^^^

If the time to maturity is very small (approaching zero), return the face value directly.

.. ipython:: python
    :okexcept:
    
    import math

    face_value = 100
    annual_yield = 0.03
    time_to_maturity = 3 / 365
    
    present_value = face_value * math.exp(-annual_yield * time_to_maturity)
    print(round(present_value, 2))



Example Calculation
^^^^^^^^^^^^^^^^^^^

Let's go through an example:

- Face Value: £1,000
- Annual Yield: 4% (0.04)
- Maturity Date: 2025-02-19
- Settlement Date: 2025-02-16

Calculate Time to Maturity:

Days to Maturity: 

.. ipython:: python
    :okexcept:
    
    from datetime import datetime
    datetime(2025, 2, 20) - datetime(2025, 2, 17)

If we assume it's not a leap year, the year Length is 365,

Time to Maturity: 

.. math:: \frac{3}{365} \approx 0.0082 \text{ years}

.. ipython:: python
    :okexcept:
    
    (datetime(2025, 2, 20) - datetime(2025, 2, 17)).days / 365

Compute Price:

Using the continuous compounding formula:

.. math::

    P = 1000 \cdot e^{-0.04 \cdot 0.0082} \approx 1000 \cdot e^{-0.000328} \approx 1000 \cdot 0.999672 \approx 999.67

.. ipython:: python
    :okexcept:
    
    time_to_maturity = (datetime(2025, 2, 20) - datetime(2025, 2, 17)).days / 365
    print(f"The time to maturity is {time_to_maturity}")

    exp_factor = -0.04 * time_to_maturity
    print(exp_factor)

    exp_value = math.exp(exp_factor)
    print(exp_value)

    face_value = 1000
    reval_price = round(face_value * exp_value, 2)
    print(f"The theoretical price of the zero-coupon gilt is £{reval_price}")
    
