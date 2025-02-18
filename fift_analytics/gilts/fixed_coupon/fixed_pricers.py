from datetime import datetime
from typing import List, Optional


def calculate_fixed_coupon_gilt_price_with_curve(
    face_value: float,
    annual_coupon_rate: float,
    settlement_date: str,
    maturity_date: str,
    bond_curve: List[float],
    day_count_convention: str = "Actual/Actual",
    coupon_frequency: int = 2,
) -> float:
    """
    Calculate the theoretical price of a fixed coupon gilt using a generic bond curve.
    
    :param face_value: The face value (maturity value) of the bond.
    :type face_value: float
    :param annual_coupon_rate: The annual coupon rate as a decimal (e.g., 0.05 for 5%).
    :type annual_coupon_rate: float
    :param settlement_date: The settlement date in 'YYYY-MM-DD' format.
    :type settlement_date: str
    :param maturity_date: The maturity date in 'YYYY-MM-DD' format.
    :type maturity_date: str
    :param bond_curve: A list of discount factors or yields for specific maturities (e.g., zero-coupon rates).
                       The length of this list must match the number of periods until maturity.
                       Each entry corresponds to the yield for one period.
    :type bond_curve: List[float]
    :param day_count_convention: The day count convention used for calculating time periods (default is "Actual/Actual").
                                 Supported values are "Actual/Actual", "30/360", and "Actual/365".
    :type day_count_convention: str
    :param coupon_frequency: Number of coupon payments per year (e.g., 1 for annual, 2 for semi-annual, 4 for quarterly).
                             Default is 2 for semi-annual payments.
    :type coupon_frequency: int
    :return: The theoretical price of the fixed coupon gilt rounded to 2 decimal places.
    :rtype: float
    
    Example::
        >>> calculate_fixed_coupon_gilt_price_with_curve(
        ...     face_value=1000,
        ...     annual_coupon_rate=0.05,
        ...     settlement_date="2025-02-17",
        ...     maturity_date="2035-02-17",
        ...     bond_curve=[0.03] * 20,  # Flat yield curve with semi-annual periods
        ...     day_count_convention="Actual/Actual",
        ... )
        1157.65
    """
    
    # Parse dates
    settlement_date = datetime.strptime(settlement_date, "%Y-%m-%d")
    maturity_date = datetime.strptime(maturity_date, "%Y-%m-%d")
    
    # Validate inputs
    if face_value <= 0:
        raise ValueError("Face value must be positive.")
    
    if annual_coupon_rate < 0:
        raise ValueError("Annual coupon rate must be non-negative.")
    
    if len(bond_curve) == 0:
        raise ValueError("Bond curve must not be empty.")
    
    if maturity_date <= settlement_date:
        raise ValueError("Maturity date must be after the settlement date.")
    
    # Calculate total number of periods and time per period based on coupon frequency
    total_periods = calculate_total_periods(settlement_date, maturity_date, coupon_frequency, day_count_convention)
    
    if len(bond_curve) < total_periods:
        raise ValueError("Bond curve must have at least as many entries as the number of periods until maturity.")
    
    # Calculate periodic coupon payment
    periodic_coupon_rate = annual_coupon_rate / coupon_frequency
    periodic_coupon_payment = face_value * periodic_coupon_rate
    
    # Initialize bond price
    price = 0.0
    
    # Calculate present value of coupons using bond curve yields
    for i in range(1, total_periods + 1):
        discount_rate = bond_curve[i - 1] / coupon_frequency
        discount_factor = (1 + discount_rate) ** i
        price += periodic_coupon_payment / discount_factor
    
    # Add present value of face value at maturity using the last discount rate in the bond curve
    final_discount_rate = bond_curve[total_periods - 1] / coupon_frequency
    final_discount_factor = (1 + final_discount_rate) ** total_periods
    price += face_value / final_discount_factor
    
    # Round intermediate result to 6 decimal places and final result to 2 decimal places
    price = round(price, 6)
    
    return round(price, 2)


def calculate_total_periods(
    settlement_date: datetime,
    maturity_date: datetime,
    coupon_frequency: int,
    day_count_convention: str,
) -> int:
    """
    Calculate the total number of periods between settlement and maturity dates based on the day count convention.
    
    :param settlement_date: Settlement date as a datetime object.
    :type settlement_date: datetime
    :param maturity_date: Maturity date as a datetime object.
    :type maturity_date: datetime
    :param coupon_frequency: Number of coupon payments per year (e.g., 1 for annual, 2 for semi-annual, 4 for quarterly).
                             Default is 2 for semi-annual payments.
    :type coupon_frequency: int
    :param day_count_convention: The day count convention used for calculating time periods.
                                 Supported values are:
                                 - "Actual/Actual": Uses actual days in each year.
                                 - "30/360": Assumes each month has 30 days and each year has 360 days.
                                 - "Actual/365": Uses actual days divided by 365.
                                 
    :type day_count_convention: str
    :return: Total number of periods until maturity.
    :rtype: int
    """
    # Validate inputs
    if day_count_convention not in ["Actual/Actual", "30/360", "Actual/365"]:
        raise ValueError("Unsupported day count convention. Use 'Actual/Actual', '30/360', or 'Actual/365'.")
    
    if settlement_date >= maturity_date:
        raise ValueError("Maturity date must be after the settlement date.")
    
    # Calculate total years to maturity based on the day count convention
    if day_count_convention == "Actual/Actual":
        # Use actual days divided by the actual number of days in each year
        total_days = (maturity_date - settlement_date).days
        year_length = 366 if is_leap_year(settlement_date.year) else 365
        total_years = total_days / year_length
    
    elif day_count_convention == "30/360":
        # Assume each month has 30 days and each year has 360 days
        total_years = calculate_30_360_years(settlement_date, maturity_date)
    
    elif day_count_convention == "Actual/365":
        # Use actual days divided by 365
        total_days = (maturity_date - settlement_date).days
        total_years = total_days / 365.0
    
    # Calculate total periods based on coupon frequency
    total_periods = int(total_years * coupon_frequency)
    
    return total_periods


def is_leap_year(year: int) -> bool:
    """
    Check if a given year is a leap year.

    :param year: Year to check.
    :type year: int
    :return: True if leap year, False otherwise.
    :rtype: bool
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def calculate_30_360_years(start_date: datetime, end_date: datetime) -> float:
    """
    Calculate the number of years between two dates using the 30/360 day count convention.

    :param start_date: Start date as a datetime object.
    :type start_date: datetime
    :param end_date: End date as a datetime object.
    :type end_date: datetime
    :return: Total years between the two dates using the 30/360 convention.
    :rtype: float
    """
    start_day = min(start_date.day, 30)
    end_day = min(end_date.day, 30)

    years = end_date.year - start_date.year
    months = end_date.month - start_date.month
    days = end_day - start_day

    return (years * 360 + months * 30 + days) / 360.0
