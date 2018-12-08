from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES = [
    'haversine>=1.0.1',
    'xmltodict==0.11.0',
    'requests>=2.20.0',
    'pytz>=2018.04',
    'dateparser',
]

setup(
    name="georss_client",
    version="0.4",
    author="Malte Franken",
    author_email="coding@subspace.de",
    description="A GeoRSS client library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/exxamalte/python-georss-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIRES
)
