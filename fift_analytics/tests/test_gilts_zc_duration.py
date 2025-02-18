import pytest
from fift_analytics.gilts.zero_coupon.zc_duration import calculate_zero_coupon_bond_duration  # Replace with your actual module name

def test_macaulay_duration():
    duration = calculate_zero_coupon_bond_duration(5, 0.05, "Macaulay", 2)
    assert duration == 5.0

def test_modified_duration_semi_annual():
    duration = calculate_zero_coupon_bond_duration(5, 0.05, "Modified", 2)
    assert pytest.approx(duration, rel=1e-6) == 4.878048780487805

def test_modified_duration_annual():
    duration = calculate_zero_coupon_bond_duration(5, 0.05, "Modified", 1)
    assert pytest.approx(duration, rel=1e-6) == 4.761904761904762

def test_continuous_compounding():
    duration = calculate_zero_coupon_bond_duration(5, 0.05, "Modified", None)
    assert duration == 5.0

def test_negative_yield():
    duration = calculate_zero_coupon_bond_duration(5, -0.01, "Modified", 2)
    assert pytest.approx(duration, rel=1e-6) == 5.025125628140703

def test_zero_yield():
    duration = calculate_zero_coupon_bond_duration(5, 0, "Modified", 2)
    assert duration == 5.0

def test_very_short_maturity():
    duration = calculate_zero_coupon_bond_duration(0.1, 0.05, "Modified", 2)
    assert pytest.approx(duration, rel=1e-6) == 0.09975062344139651

def test_very_long_maturity():
    duration = calculate_zero_coupon_bond_duration(30, 0.05, "Modified", 2)
    assert pytest.approx(duration, rel=1e-6) == 29.268292682926827

def test_invalid_duration_type():
    with pytest.raises(ValueError):
        calculate_zero_coupon_bond_duration(5, 0.05, "Invalid", 2)

def test_negative_time_to_maturity():
    with pytest.raises(ValueError):
        calculate_zero_coupon_bond_duration(-1, 0.05, "Modified", 2)

def test_zero_time_to_maturity():
    with pytest.raises(ValueError):
        calculate_zero_coupon_bond_duration(0, 0.05, "Modified", 2)

def test_invalid_compounding_frequency():
    with pytest.raises(ValueError):
        calculate_zero_coupon_bond_duration(5, 0.05, "Modified", 0)

def test_extremely_high_yield():
    duration = calculate_zero_coupon_bond_duration(5, 1.0, "Modified", 2)  # 100% yield
    assert pytest.approx(duration, rel=1e-6) == 2.5

def test_extremely_low_yield():
    duration = calculate_zero_coupon_bond_duration(5, 0.0001, "Modified", 2)  # 0.01% yield
    assert pytest.approx(duration, rel=1e-6) == 4.999875015624219

def test_macaulay_equals_modified_for_continuous():
    macaulay = calculate_zero_coupon_bond_duration(5, 0.05, "Macaulay", None)
    modified = calculate_zero_coupon_bond_duration(5, 0.05, "Modified", None)
    assert macaulay == modified

