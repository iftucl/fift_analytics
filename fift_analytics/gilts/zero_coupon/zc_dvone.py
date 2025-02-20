"""
DV01 Zero Coupon
================

DV01, the dollar change in the bond's value for a 1 basis point change in yield.

Current implementation relies on:

- Valuate Bond Price at provided yield
- Revaluate Bond Price at Provided Yield + 1bps

"""

from datetime import datetime
from typing import Optional

from fift_analytics.gilts.zero_coupon.zc_pricers import get_zero_coupon_gilt_price


def calculate_zero_coupon_bond_dv01(
    face_value: float,
    yield_to_maturity: float,
    maturity_date: str,
    settlement_date: Optional[str] = None,
    maturity_threshold: float = 7/365,
    n_decimals: int | None = None
) -> float:
    """
    Calculate the DV01 of a zero-coupon bond using the get_zero_coupon_gilt_price function.
    
    :param face_value: Face value of the bond.
    :param yield_to_maturity: Annual yield to maturity as a decimal (e.g., 0.05 for 5%).
    :param maturity_date: The maturity date of the bond in 'YYYY-MM-DD' format.
    :param settlement_date: The settlement date in 'YYYY-MM-DD' format. Defaults to today if not provided.
    :param maturity_threshold: Threshold (in years) below which DV01 is considered zero (default is 7 days).
    :param n_decimals: Decimal precision of the returned dv01.
    :return: DV01 of the zero-coupon bond.
    """
    # Calculate time to maturity
    if settlement_date is None:
        settlement_date = datetime.now().strftime('%Y-%m-%d')
    settlement_date_obj = datetime.strptime(settlement_date, '%Y-%m-%d')
    maturity_date_obj = datetime.strptime(maturity_date, '%Y-%m-%d')
    time_to_maturity = (maturity_date_obj - settlement_date_obj).days / 365.0

    if time_to_maturity <= 0:
        raise ValueError("Time to maturity must be positive.")
    
    if time_to_maturity <= maturity_threshold:
        return 0.0

    # Calculate the current price
    price = get_zero_coupon_gilt_price(face_value, yield_to_maturity, maturity_date, settlement_date)

    # Calculate price after 1bp increase in yield
    price_up = get_zero_coupon_gilt_price(face_value, yield_to_maturity + 0.0001, maturity_date, settlement_date)

    # Calculate DV01
    dv01 = price - price_up
    
    if not n_decimals:
        return round(dv01, 2)
    
    return dv01

    

