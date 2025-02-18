"""
DV01 Zero Coupon
================

DV01, the dollar change in the bond's value for a 1 basis point change in yield.

Implementation of:

DV01 = T / [100(1 + y/2)^(2T + 1)]

"""

import math

def calculate_zero_coupon_bond_dv01(
        face_value: float,
        yield_to_maturity: float,
        time_to_maturity: float,
        compounding_frequency: int = 2,
        maturity_threshold: float = 7/365
    ) -> float:
    """
    Calculate the DV01 of a zero-coupon bond.
    
    :param face_value: Face value of the bond.
    :param yield_to_maturity: Annual yield to maturity as a decimal (e.g., 0.05 for 5%).
    :param time_to_maturity: Time to maturity in years.
    :param compounding_frequency: Number of compounding periods per year (default is 2 for semi-annual).
    :param maturity_threshold: Threshold (in years) below which DV01 is considered zero (default is 7 days).    
    :return: DV01 of the zero-coupon bond.

    :Example:
        >>> from fift_analytics.gilts import calculate_zero_coupon_bond_dv01
        >>> face_value = 1000000  # $1 million
        >>> yield_to_maturity = 0.05  # 5%
        >>> time_to_maturity = 10  # 10 years
        >>> dv01 = calculate_zero_coupon_bond_dv01(face_value, yield_to_maturity, time_to_maturity)
        >>> print(f"DV01 of the zero-coupon bond: ${dv01:.2f}")
    """
    if time_to_maturity <= 0:
        raise ValueError("Time to maturity must be positive.")
    # we return a zero for bond close to maturity    
    if maturity_threshold > time_to_maturity:
        return 0
    # Convert annual yield to periodic yield
    periodic_yield = yield_to_maturity / compounding_frequency    
    # Calculate the number of compounding periods
    n = time_to_maturity * compounding_frequency    
    # Calculate the price of the bond
    price = face_value / math.pow(1 + periodic_yield, n)    
    # Calculate DV01
    dv_one = (time_to_maturity * price) / (100 * math.pow(1 + periodic_yield, n + 1))
    
    return dv_one

