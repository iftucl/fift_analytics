from datetime import datetime
import math
from typing import Optional
from pydantic import validate_call

@validate_call
def get_zero_coupon_gilt_price(
    face_value: float, annual_yield: float, maturity_date: str, settlement_date: Optional[str] = None
) -> float:
    """
    Calculate the theoretical price of a zero-coupon gilt using continuous compounding.
    
    :param face_value: The face value (maturity value) of the bond.
    :type face_value: float
    :param annual_yield: The annual yield to maturity as a decimal (e.g., 0.04 for 4% or -0.01 for -1%).
    :type annual_yield: float
    :param maturity_date: The maturity date of the bond in 'YYYY-MM-DD' format.
    :type maturity_date: str
    :param settlement_date: The settlement date in 'YYYY-MM-DD' format. Defaults to today if not provided.
    :type settlement_date: Optional[str]
    :raises ValueError: If inputs are invalid (e.g., negative face value or invalid dates).
    :return: The theoretical price of the zero-coupon gilt rounded to 2 decimal places.
    :rtype: float
    
    :Example:
        >>> face_value = 1000  # £1,000 face value
        >>> annual_yield = -0.01  # -1% annual yield
        >>> maturity_date = "2025-02-19"  # Maturity date: February 17, 2035
        >>> settlement_date = "2025-02-16"  # Settlement date: February 17, 2025
        >>> price = get_zero_coupon_gilt_price(face_value, annual_yield, maturity_date, settlement_date)
        >>> print(f"The theoretical price of the zero-coupon gilt is: £{price:.2f}")
    """
    # Validate inputs
    validate_inputs(face_value, maturity_date, settlement_date)

    # Parse and calculate time to maturity
    settlement_date_obj = parse_settlement_date(settlement_date)
    maturity_date_obj = parse_maturity_date(maturity_date)
    time_to_maturity = calculate_time_to_maturity(settlement_date_obj, maturity_date_obj)
    if time_to_maturity == 0:
        # this is the case when days to maturity are <3. we do't try to calculate but we return face value
        # as the bond due to T+1 settlement would be unlikely to trade or would have large delivery risk
        return face_value
    # Compute price using continuous compounding formula
    price = compute_continuous_price(face_value, annual_yield, time_to_maturity)

    return price


def validate_inputs(face_value: float, maturity_date: str, settlement_date: Optional[str]) -> None:
    """
    Validate input parameters for correctness.
    
    :param face_value: Face value of the bond.
    :param maturity_date: Maturity date in 'YYYY-MM-DD' format.
    :param settlement_date: Settlement date in 'YYYY-MM-DD' format or None.
    :raises ValueError: If any input is invalid (e.g., negative face value or invalid dates).
    """
    if face_value <= 0:
        raise ValueError("Face value must be positive.")
    
    try:
        datetime.strptime(maturity_date, '%Y-%m-%d')
        if settlement_date:
            datetime.strptime(settlement_date, '%Y-%m-%d')
    except ValueError as e:
        raise ValueError("Invalid date format. Dates must be in 'YYYY-MM-DD' format.") from e


def parse_settlement_date(settlement_date: Optional[str]) -> datetime:
    """
    Parse and return the settlement date. Defaults to today if not provided.

    :param settlement_date: Settlement date in 'YYYY-MM-DD' format or None.
    :return: Settlement date as a datetime object.
    """
    if settlement_date is None:
        return datetime.now()
    
    return datetime.strptime(settlement_date, '%Y-%m-%d')


def parse_maturity_date(maturity_date: str) -> datetime:
    """
    Parse and return the maturity date.

    :param maturity_date: Maturity date in 'YYYY-MM-DD' format.
    :return: Maturity date as a datetime object.
    """
    return datetime.strptime(maturity_date, '%Y-%m-%d')


def calculate_time_to_maturity(settlement_date: datetime, maturity_date: datetime) -> float:
    """
    Calculate time to maturity in years using Actual/Actual (ISMA) day count convention.

    :param settlement_date: Settlement date as a datetime object.
    :param maturity_date: Maturity date as a datetime object.
    :return: Time to maturity in years.
    
    :raises ValueError: If the maturity date is earlier than or equal to the settlement date.
    """
    if maturity_date <= settlement_date:
        raise ValueError("Maturity date must be after the settlement date.")
    
    days_to_maturity = (maturity_date - settlement_date).days

    if days_to_maturity < 3:
        # we return zero for days to maturity less then 3 and we handle this in the pricer to yield the face value
        return 0

    # Determine if it's a leap year for Actual/Actual convention
    year_length = 366 if is_leap_year(settlement_date.year) else 365
    
    return days_to_maturity / year_length


def is_leap_year(year: int) -> bool:
    """
    Check if a given year is a leap year.

    :param year: Year to check.
    :return: True if leap year, False otherwise.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)



@validate_call
def compute_continuous_price(face_value: float, annual_yield: float, time_to_maturity: float) -> float:
    """
    Compute the price of a zero-coupon gilt using continuous compounding.

    :param face_value: Face value of the bond.
    :type face_value: float
    :param annual_yield: Annual yield to maturity as a decimal (e.g., 0.04 for 4% or -0.01 for -1%).
    :type annual_yield: float
    :param time_to_maturity: Time to maturity in years.
    :type time_to_maturity: float
    :return: The price of the zero-coupon gilt rounded to 2 decimal places.
    :rtype: float
    
    **Calculation Steps**:
        - If time_to_maturity is very small (approaching zero), return face value directly.
        - Compute intermediate result using the continuous compounding formula:
          `P = F * exp(-r * t)`
        - Round intermediate result to six decimal places for precision.
        - Round final result to two decimal places for financial reporting standards.
    
    :Example:
        >>> compute_continuous_price(1000, -0.01, 10)
        1051.27
    """
    # Handle edge cases
    if time_to_maturity < 0:
        raise ValueError("Time to maturity cannot be negative.")
    
    if time_to_maturity == 0 or time_to_maturity < 1 / 365:  # Less than one day
        return round(face_value, 2)

    # Continuous compounding formula: P = F * e^(-r * t)
    intermediate_price = face_value * math.exp(-annual_yield * time_to_maturity)

    # Round intermediate result to 6 decimal places
    intermediate_price = round(intermediate_price, 6)

    # Round final result to 2 decimal places (nearest penny)
    final_price = round(intermediate_price, 2)

    return final_price
