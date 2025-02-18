from datetime import datetime, date
from typing import List, Optional
from dateutil.relativedelta import relativedelta

def calculate_fixed_coupon_gilt_price_dmo(
    face_value: float,
    annual_coupon_rate: float,
    settlement_date: str,
    maturity_date: str,
    nominal_redemption_yield: float,
) -> float:
    """
    Calculate the dirty price of a conventional gilt per £100 nominal,
    using the DMO's price/yield formula and settlement conventions.

    :param face_value: The face value of the gilt (£100).
    :type face_value: float
    :param annual_coupon_rate: Annual coupon rate (decimal, e.g., 0.05 for 5%).
    :type annual_coupon_rate: float
    :param settlement_date: Settlement date in 'YYYY-MM-DD' format.
    :type settlement_date: str
    :param maturity_date: Maturity date in 'YYYY-MM-DD' format.
    :type maturity_date: str
    :param nominal_redemption_yield: Nominal redemption yield (decimal).
    :type nominal_redemption_yield: float
    :raises ValueError: If inputs are invalid.
    :return: Dirty price per £100 nominal, rounded to the nearest penny.
    :rtype: float
    """
    # 1. Input Validation and Date Conversion
    try:
        settlement_date_dt = datetime.strptime(settlement_date, "%Y-%m-%d").date()
        maturity_date_dt = datetime.strptime(maturity_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    if settlement_date_dt >= maturity_date_dt:
        raise ValueError("Settlement date must be before maturity date.")

    if face_value != 100:
        raise ValueError("Face value must be equal to 100, as DMO formula is per £100 nominal.")

    # 2. Parameters from the DMO formula
    c = annual_coupon_rate  # Coupon per £100 nominal
    y = nominal_redemption_yield  # Nominal redemption yield
    f = 2  # Coupons per year (semi-annual)
    v = 1 / (1 + (y / f))

    # 3. Determine Quasi-Coupon Dates
    # a. Find the prior quasi-coupon date
    month_delta = 6 if maturity_date_dt.month > 6 else 0
    year = maturity_date_dt.year
    prior_coupon_month = 6 if maturity_date_dt.month > 6 else 12
    prior_coupon_year = year if maturity_date_dt.month > 6 else year -1

    if prior_coupon_month == 6:
        prior_quasi_coupon_date = date(prior_coupon_year, 6, maturity_date_dt.day)
    else:
        prior_quasi_coupon_date = date(prior_coupon_year, 12, maturity_date_dt.day)
        
    # Find the next quasi-coupon date
    if maturity_date_dt.month > 6:
        next_quasi_coupon_date = date(maturity_date_dt.year + 1, 6, maturity_date_dt.day)
    else:
        next_quasi_coupon_date = date(maturity_date_dt.year, 6, maturity_date_dt.day)

    # 4. Calculate 'r' and 's' (Actual/Actual Day Count)
    r = (next_quasi_coupon_date - settlement_date_dt).days
    s = (next_quasi_coupon_date - prior_quasi_coupon_date).days

    # 5. Number of Full Quasi-Coupon Periods (n)
    # Calculate the number of *full* quasi-coupon periods from the *next* quasi-coupon date to the maturity date.
    n = 0
    current_date = next_quasi_coupon_date
    while current_date < maturity_date_dt:
        current_date += relativedelta(months=+6)
        n += 1

    if current_date != maturity_date_dt:
        n -= 1

    # Calculate the cashflows at the next two quasi coupon dates
    d1 = annual_coupon_rate / 2 #Regular coupon cashflow

    # The coupon cashflow is zero if the settlement date is after the ex-dividend date
    # 6. Apply DMO Price/Yield Formula
    if n >= 1:
        price = (
            (d1 * v * ((1 - v**n) / (1 - v))) + (100 * v**n)
        ) * v**(r/s)
    else:
        price = d1 * v**(r / s)
    # 7. Rounding to nearest penny
    price = round(price, 2)

    return price

