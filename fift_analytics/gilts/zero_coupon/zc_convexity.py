"""
Convexity Zero-Coupon Bond
==========================

[DMO Yield Curve Methodologies](https://www.dmo.gov.uk/media/nozauetl/yldcrv.pdf)

"""
from pydantic import validate_call

@validate_call
def calculate_zero_coupon_bond_convexity(
    time_to_maturity: float,
    annual_yield: float,
    compounding_frequency: int = 2  # Default to semi-annual compounding
) -> float:
    """
    Calculate the convexity of a zero-coupon bond using DMO-aligned methodology.
    
    :param time_to_maturity: Time to maturity in years.
    :type time_to_maturity: float
    :param annual_yield: Yield-to-maturity as a decimal (e.g., 0.05 for 5%, -0.01 for -1%).
    :type annual_yield: float
    :param compounding_frequency: Number of compounding periods per year (default is 2 for semi-annual).
    :type compounding_frequency: int
    :return: Convexity of the zero-coupon bond.
    :rtype: float
    
    Example::
        >>> calculate_zero_coupon_bond_convexity(5, 0.05)
        26.455026455026455
    """
    # Validate inputs
    if time_to_maturity <= 0:
        raise ValueError("Time to maturity must be positive.")
    
    # Adjust yield and time-to-maturity for compounding frequency
    periodic_yield = annual_yield / compounding_frequency
    denominator = (1 + periodic_yield) ** 2
    
    # Convexity formula
    convexity = (time_to_maturity * (time_to_maturity + 1)) / denominator
    
    return convexity
