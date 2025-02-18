from typing import Optional, Literal
from pydantic import validate_call

@validate_call
def calculate_zero_coupon_bond_duration(
    time_to_maturity: float,
    ytm: float,
    duration_type: Literal["Macaulay", "Modified"],
    compounding_frequency: Optional[int] = None
) -> dict:
    """
    Calculate the Macaulay or Modified durations of a zero-coupon bond, allowing for negative yields.
    
    :param time_to_maturity: Time to maturity in years.
    :type time_to_maturity: float
    :param ytm: Yield-to-maturity as a decimal (e.g., 0.05 for 5%, -0.01 for -1%).
    :type ytm: float
    :param duration_type: type of duration calculated: can be only "Macaulay", "Modified".
    :type duration_type: str
    :param compounding_frequency: Number of compounding periods per year (e.g., 1 for annual, 2 for semi-annual).
                                  If None, assumes continuous compounding.
    :type compounding_frequency: Optional[int]
    :return: The calculated duration
    :rtype: float
    
    Example::
        >>> calculate_zero_coupon_bond_duration(5, -0.01, "Modified", 2)
        5.025125628140703
    """
    # Validate inputs
    if time_to_maturity <= 0:
        raise ValueError("Time to maturity must be positive.")
    
    # Calculate Macaulay Duration
    if duration_type == "Macaulay":
        return time_to_maturity
    
    # Calculate Modified Duration
    if compounding_frequency is None:
        # Continuous compounding case
        return time_to_maturity
    else:
        # Discrete compounding case (supports negative yields)
        modified_duration = time_to_maturity / (1 + ytm / compounding_frequency)
    
    return modified_duration