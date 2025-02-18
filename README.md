<p align="center">
    <a href=""><img src="./docs/source/_static/fift_analytics_banner.png" alt="IFTGBanner-BigData-IFT"></a>
</p>
<p align="center">
    <em>IFT Fixed Income GILTS Analytics Python Package</em>
</p>

|||||
|--------------------------------|--------------------------------------|---------|-----|
|**Build**|![Build Status](https://github.com/iftucl/fift_analytics/actions/workflows/build.yml/badge.svg)|**Documentation**|[![fift_analytics Documentation](https://shields.io/badge/fift_analytics-Documentation-blue?logo=Sphinx)](https://iftucl.github.io/fift_analytics/)|
|**Unit Test**|[![Unit Test](https://github.com/iftucl/fift_analytics/actions/workflows/test.yml/badge.svg)](https://github.com/iftucl/fift_analytics/actions/workflows/test.yml)|
|**Coverage**|[![Coverage](https://codecov.io/github/iftucl/fift_analytics/coverage.svg?branch=main)](https://codecov.io/gh/iftucl/fift_analytics)|
|**Linting**|![Linters](https://github.com/iftucl/fift_analytics/actions/workflows/linting.yml/badge.svg)|

# fift_analytics

**IFT  Fixed Income Analytics (FIFT)** is a python package that provides abstraction functionalities used model the GILTS Sovereign Bonds. This is used for didactical purposes in the Big Data in Quantitative Finance module @uclift.

## Main Features

- zero coupon bonds : abstraction to model gilts zero coupon bonds.

## How to get

The artifacts of this repository are not yet pushed to pypi.
However, we provide some options to install and use this python library:

### whl built

the .whl and tar files are available for download on the Build Pipeline within this repo. As the package has not yet reached a stable state we won't publish to pypi.

### poetry

from the command line of your project:

```bash

poetry add git+https://github.com/iftucl/fift_analytics.git

```