import pytest
from datetime import datetime
from fift_analytics.gilts.zero_coupon.zc_pricers import (
    get_zero_coupon_gilt_price,
    validate_inputs,
    parse_settlement_date,
    parse_maturity_date,
    calculate_time_to_maturity,
    is_leap_year,
    compute_continuous_price,
)


# Test compute_continuous_price
def test_compute_continuous_price_positive_yield():
    assert compute_continuous_price(1000, 0.03, 10) == 740.82


def test_compute_continuous_price_negative_yield():
    assert compute_continuous_price(1000, -0.01, 10) == 1105.17


def test_compute_continuous_price_zero_yield():
    assert compute_continuous_price(1000, 0.0, 10) == 1000.00


# Test is_leap_year
def test_is_leap_year():
    assert is_leap_year(2024) is True  # Leap year
    assert is_leap_year(2023) is False  # Non-leap year
    assert is_leap_year(2000) is True  # Leap year divisible by 400
    assert is_leap_year(1900) is False  # Not a leap year divisible by 100


# Test calculate_time_to_maturity
def test_calculate_time_to_maturity_normal_case():
    settlement_date = datetime.strptime("2025-02-17", "%Y-%m-%d")
    maturity_date = datetime.strptime("2035-02-17", "%Y-%m-%d")
    assert calculate_time_to_maturity(settlement_date, maturity_date) == 10.0


def test_calculate_time_to_maturity_with_leap_year():
    settlement_date = datetime.strptime("2024-02-17", "%Y-%m-%d")
    maturity_date = datetime.strptime("2034-02-17", "%Y-%m-%d")
    assert calculate_time_to_maturity(settlement_date, maturity_date) == pytest.approx(10.0027, rel=1e-4)


def test_calculate_time_to_maturity_invalid_dates():
    settlement_date = datetime.strptime("2035-02-17", "%Y-%m-%d")
    maturity_date = datetime.strptime("2025-02-17", "%Y-%m-%d")
    with pytest.raises(ValueError, match="Maturity date must be after the settlement date."):
        calculate_time_to_maturity(settlement_date, maturity_date)


# Test parse_settlement_date
def test_parse_settlement_date_with_provided_date():
    settlement_date = parse_settlement_date("2025-02-17")
    assert settlement_date == datetime.strptime("2025-02-17", "%Y-%m-%d")


def test_parse_settlement_date_with_default_today(mocker):
    date_today = datetime.now().strftime("%Y-%m-%d")
    mock_today = datetime.strptime(date_today, "%Y-%m-%d")
    settlement_date = parse_settlement_date(None)
    assert datetime.strptime(settlement_date.strftime("%Y-%m-%d"), "%Y-%m-%d") == mock_today


# Test parse_maturity_date
def test_parse_maturity_date_valid():
    maturity_date = parse_maturity_date("2035-02-17")
    assert maturity_date == datetime.strptime("2035-02-17", "%Y-%m-%d")


# Test validate_inputs
def test_validate_inputs_valid_case():
    validate_inputs(1000, "2035-02-17", "2025-02-17")  # Should not raise any errors


def test_validate_inputs_invalid_face_value():
    with pytest.raises(ValueError, match="Face value must be positive."):
        validate_inputs(-1000, "2035-02-17", "2025-02-17")


def test_validate_inputs_invalid_dates_format():
    with pytest.raises(ValueError, match="Invalid date format. Dates must be in 'YYYY-MM-DD' format."):
        validate_inputs(1000, "35/02/2035", "2025/02/17")


# Test get_zero_coupon_gilt_price (integration tests)
def test_get_zero_coupon_gilt_price_positive_yield():
    price = get_zero_coupon_gilt_price(1000, 0.03, "2035-02-17", "2025-02-17")
    assert price == 740.7


def test_get_zero_coupon_gilt_price_negative_yield():
    price = get_zero_coupon_gilt_price(1000, -0.01, "2035-02-17", "2025-02-17")
    assert price == 1105.23

def test_get_zero_coupon_gilt_price_invalid_dates():
    with pytest.raises(ValueError, match="Maturity date must be after the settlement date."):
        get_zero_coupon_gilt_price(1000, 0.03, "2025-02-17", "2035-02-17")


def test_get_zero_coupon_gilt_price_invalid_face_value():
    with pytest.raises(ValueError, match="Face value must be positive."):
        get_zero_coupon_gilt_price(-1000, 0.03, "2035-02-17", "2025-02-17")
