"""
Extrapolate Zero Coupon Curve
==============================

.. currentmodule:: fift_analytics.gilts.zero_coupon.curve_yield_extrapolation

These functions are used to interpolate or extrapolate yields from
zero coupon bond curve.

.. autosummary::
   :toctree: generated/

   derive_yield_from_zero_curve

"""
from pydantic import validate_call

@validate_call
def derive_yield_from_zero_curve(
    zero_curve: list[tuple[int, float]],
    target_maturity: float
) -> float:
    """
    Derive the implicit yield for a given maturity using a zero-coupon bond curve.

    :Formula:
    .. math:: y = y1 + ((t - t1) * (y2 - y1)) / (t2 - t1)

    Interpolates between two maturities.

    - for maturities less than 3 months, uses 3 months.
    - for maturities greater than largest tenor point on the curve, it extrapolates.

    
    :param zero_curve: A list of tuples representing the zero-coupon bond curve.
                       Each tuple contains (maturity_in_months, annual_yield).
                       Example: [(3, 0.01), (6, 0.015), (12, 0.02), (18, 0.025)]
    :type zero_curve: list
    :param target_maturity: The target maturity in months for which to derive the yield.
    :type target_maturity: float
    :return: The interpolated or extrapolated yield for the given maturity.
    :rtype: float
    
    :Example:
        >>> zero_curve = [(3, 0.01), (6, 0.015), (12, 0.02), (18, 0.025)]
        >>> derive_yield_from_zero_curve(zero_curve, 9)
        0.0175
        >>> derive_yield_from_zero_curve(zero_curve, 2)
        0.01
        >>> derive_yield_from_zero_curve(zero_curve, 24)
        0.03
    """
    # Validate inputs
    if not zero_curve or len(zero_curve) < 2:
        raise ValueError("Zero curve must contain at least two points.")
    
    if target_maturity < 0:
        raise ValueError("Target maturity must be non-negative.")
    
    # Sort zero curve by maturity in ascending order
    zero_curve = sorted(zero_curve, key=lambda x: x[0])
    
    # Handle flat yield assumption for maturities less than 3 months
    # Return yield corresponding to shortest maturity
    if target_maturity < 3:
        return zero_curve[0][1] 
    
    # Linear interpolation or extrapolation
    for i in range(len(zero_curve) - 1):
        t1, y1 = zero_curve[i]
        t2, y2 = zero_curve[i + 1]
        
        if t1 <= target_maturity <= t2:
            # Linear interpolation formula
            interpolated_yield = y1 + ((y2 - y1) * (target_maturity - t1)) / (t2 - t1)
            return interpolated_yield
    
    # Extrapolate if target maturity is beyond the longest point on the curve
    t_last, y_last = zero_curve[-2]
    t_final, y_final = zero_curve[-1]
    
    extrapolated_yield = y_last + ((y_final - y_last) * (target_maturity - t_last)) / (t_final - t_last)
    
    return extrapolated_yield
