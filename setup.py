"""Setup of georss_client library."""

from setuptools import find_packages, setup

from georss_client.__version__ import __version__

NAME = "georss_client"
AUTHOR = "Malte Franken"
AUTHOR_EMAIL = "coding@subspace.de"
DESCRIPTION = "A GeoRSS client library."
URL = "https://github.com/exxamalte/python-georss-client"

REQUIRES = [
    "haversine>=2.8.1",
    "xmltodict>=0.13.0",
    "requests>=2.31.0",
    "dateparser>=1.2.0",
]

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=__version__,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license="Apache-2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(exclude=("tests*",)),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIRES,
)
