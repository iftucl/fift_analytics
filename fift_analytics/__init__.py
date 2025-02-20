from __future__ import annotations

import importlib
import typing

__version__ = "0.0.0"
__version_tuple__ = (0, 0, 0)

__doc__ = """
fift_analytics python package
==============================

Python package developed and maintained by Big Data in Quantitative Finance
Institute for Finance and Technology - University College London.


This python package delivers the main abstraction utilities to perform analytics tasks on GILTS Fixed Income Sovereign Bonds

Public API
----------

Main Features:

- GILTS Zero Coupon Bond: main methods to perform analytics on Zero Coupon GILTS

"""

from fift_analytics.gilts import zero_coupon


__all__ = [
    "zero_coupon",
]