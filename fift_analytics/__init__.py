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

The modules exported within this document are considered part of the :py:mod:`fift_analytics` public api and are maintained and stable abstraction ready to use.

Main Features
-------------
::

 zero_coupon                -- Abstraction for Zero Coupon Gilts



"""

from fift_analytics.gilts import zero_coupon


__all__ = [
    "zero_coupon",
]