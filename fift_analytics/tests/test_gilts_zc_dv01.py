import pytest
from fift_analytics.gilts.zero_coupon.zc_dvone import calculate_zero_coupon_bond_dv01
from datetime import datetime, timedelta 

def test_dv01_normal_case():
    maturity_date = datetime.strftime(datetime.now() + timedelta(days=3650), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(face_value=1000000, yield_to_maturity=0.05, maturity_date=maturity_date)
    assert pytest.approx(dv01, rel=0.001) == 606.229

def test_dv01_below_threshold():
    maturity_date = datetime.strftime(datetime.now() + timedelta(days=5), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.05, maturity_date=maturity_date)  # 5 days to maturity
    assert dv01 == 0.0

def test_dv01_at_threshold():
    maturity_date = datetime.strftime(datetime.now() + timedelta(days=6), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.05, maturity_date=maturity_date)
    assert dv01 == 0.0

def test_dv01_just_above_threshold():
    maturity_date = datetime.strftime(datetime.now() + timedelta(days=8), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.05, maturity_date=maturity_date)  # 8 days to maturity
    assert dv01 > 0.0

def test_dv01_negative_yield():
    maturity_date = datetime.strftime(datetime.now() + timedelta(days=3650), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, -0.01, maturity_date=maturity_date)
    assert pytest.approx(dv01, rel=0.001) == 1104.6199

def test_dv01_zero_yield():
    maturity_date = datetime.strftime(datetime.now() + timedelta(days=365*5), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0, maturity_date=maturity_date) # approx 5y maturity
    assert pytest.approx(dv01, rel=0.001) == 499.88

def test_dv01_very_long_maturity():
    maturity_date = datetime.strftime(datetime.now() + timedelta(days=365*30), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.05, maturity_date=maturity_date)
    assert pytest.approx(dv01, rel=0.001) == 668.39

def test_dv01_custom_threshold():
    maturity_date = datetime.strftime(datetime.now() + timedelta(days=10), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.05, maturity_date=maturity_date, maturity_threshold=5/365)
    assert dv01 > 0.0  # Should be non-zero with custom threshold

def test_dv01_zero_face_value():
    maturity_date = datetime.strftime(datetime.now() + timedelta(days=365), "%Y-%m-%d")
    with pytest.raises(ValueError):
        dv01 = calculate_zero_coupon_bond_dv01(0, 0.05, maturity_date=maturity_date)

def test_dv01_negative_time_to_maturity():
    with pytest.raises(TypeError):
        calculate_zero_coupon_bond_dv01(1000000, 0.05, -1)

def test_dv01_zero_time_to_maturity():
    maturity_date = datetime.strftime(datetime.now() - timedelta(days=365), "%Y-%m-%d")
    with pytest.raises(ValueError):
        calculate_zero_coupon_bond_dv01(1000000, 0.05, maturity_date=maturity_date)

def test_dv01_extremely_high_yield():
    maturity_date = datetime.strftime(datetime.now() + timedelta(days=3650), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 1.0, maturity_date=maturity_date)  # 100% yield
    assert dv01 > 0.0 and dv01 < 0.05  # Should be positive but less than normal case

def test_dv01_extremely_low_yield():
    maturity_date = datetime.strftime(datetime.now() + timedelta(days=3650), "%Y-%m-%d")
    dv01 = calculate_zero_coupon_bond_dv01(1000000, 0.0001, maturity_date=maturity_date)  # 0.01% yield
    assert dv01 > 998.49  # Should be higher than normal case
