import pytest
from fift_analytics.gilts.zero_coupon.curve_yield_extrapolation import derive_yield_from_zero_curve

def test_flat_yield_for_short_maturities():
    zero_curve = [(3, 0.01), (6, 0.015), (12, 0.02)]
    assert derive_yield_from_zero_curve(zero_curve, 2) == 0.01  # Flat yield for <3 months

def test_interpolation_between_two_points():
    zero_curve = [(3, 0.01), (6, 0.015), (12, 0.02)]
    result = derive_yield_from_zero_curve(zero_curve, 9)  # Between 6 and 12 months
    assert result == pytest.approx(0.0175, rel=1e-4)

def test_exact_match_on_curve_point():
    zero_curve = [(3, 0.01), (6, 0.015), (12, 0.02)]
    assert derive_yield_from_zero_curve(zero_curve, 6) == 0.015  # Exact match at 6 months

def test_extrapolation_beyond_longest_maturity():
    zero_curve = [(3, 0.01), (6, 0.015), (12, 0.02), (18, 0.025)]
    result = derive_yield_from_zero_curve(zero_curve, 24)  # Beyond the last point
    assert result == pytest.approx(0.03, rel=1e-4)

def test_extrapolation_with_negative_slope():
    zero_curve = [(3, 0.03), (6, 0.025), (12, 0.02)]
    result = derive_yield_from_zero_curve(zero_curve, 18)  # Beyond the last point
    assert result == pytest.approx(0.015, rel=1e-4)

def test_single_point_on_curve_raises_error():
    zero_curve = [(3, 0.01)]  # Only one point
    with pytest.raises(ValueError, match="Zero curve must contain at least two points."):
        derive_yield_from_zero_curve(zero_curve, 9)

def test_negative_maturity_raises_error():
    zero_curve = [(3, 0.01), (6, 0.015)]
    with pytest.raises(ValueError, match="Target maturity must be non-negative."):
        derive_yield_from_zero_curve(zero_curve, -1)

def test_unsorted_input_is_sorted_correctly():
    zero_curve = [(12, 0.02), (3, 0.01), (6, 0.015)]  # Unsorted input
    result = derive_yield_from_zero_curve(zero_curve, 9)
    assert result == pytest.approx(0.0175, rel=1e-4)

def test_flat_yield_for_exactly_3_months():
    zero_curve = [(3, 0.01), (6, 0.015)]
    assert derive_yield_from_zero_curve(zero_curve, 3) == pytest.approx(0.01)

def test_interpolation_edge_case_at_boundary():
    zero_curve = [(3, 0.01), (6, 0.015)]
    result = derive_yield_from_zero_curve(zero_curve, 4)  # Close to first boundary
    expected_yield = 0.01 + ((0.015 - 0.01) * (4 - 3)) / (6 - 3)
    assert result == pytest.approx(expected_yield)
