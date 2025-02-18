import pytest
from fift_analytics.gilts.zero_coupon.zc_dvone import calculate_zero_coupon_bond_dv01

def test_dv01_normal_case():
    dv01 = calculate_zero_coupon_bond_dv01(face_value=1000000, yield_to_maturity=0.05, time_to_maturity=10)
    assert pytest.approx(dv01, rel=0.001) == 36334.69499

def test_dv01_below_threshold():
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.05, 5/365)  # 5 days to maturity
    assert dv01 == 0.0

def test_dv01_at_threshold():
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.05, 7/365)  # Exactly 7 days to maturity
    assert dv01 == 0.0

def test_dv01_just_above_threshold():
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.05, 8/365)  # 8 days to maturity
    assert dv01 > 0.0

def test_dv01_negative_yield():
    dv01 = calculate_zero_coupon_bond_dv01(1000000, -0.01, 5)
    assert pytest.approx(dv01, rel=0.001) == 55550.15929

def test_dv01_zero_yield():
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0, 5)
    assert pytest.approx(dv01, rel=0.001) == 5000.0

def test_dv01_very_long_maturity():
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.05, 30)
    assert pytest.approx(dv01, rel=0.001) == 15119.364678

def test_dv01_custom_compounding():
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.05, 10, compounding_frequency=4)
    assert pytest.approx(dv01, rel=0.001) != 36559.9132  # Should be different from semi-annual

def test_dv01_custom_threshold():
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.05, 10/365, maturity_threshold=5/365)
    assert dv01 > 0.0  # Should be non-zero with custom threshold

def test_dv01_zero_face_value():
    dv01 = calculate_zero_coupon_bond_dv01(0, 0.05, 10)
    assert dv01 == 0.0

def test_dv01_negative_time_to_maturity():
    with pytest.raises(ValueError):
        calculate_zero_coupon_bond_dv01(1000000, 0.05, -1)

def test_dv01_zero_time_to_maturity():
    with pytest.raises(ValueError):
        calculate_zero_coupon_bond_dv01(1000000, 0.05, 0)

def test_dv01_extremely_high_yield():
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 1.0, 10)  # 100% yield
    assert dv01 > 0.0 and dv01 < 613.9132  # Should be positive but less than normal case

def test_dv01_extremely_low_yield():
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.0001, 10)  # 0.01% yield
    assert dv01 > 613.9132  # Should be higher than normal case
