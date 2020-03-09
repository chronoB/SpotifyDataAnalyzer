"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="spotifydataanalyzer",
    version="0.1",
    description="This repository is build to analyze the personal user data spotify is collecting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chronoB/SpotifyDataAnalyzer",
    author="chronoB",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="spotify data analysis",
    packages=find_packages(include=["src", "src.*"]),
    python_requires=">=3.6",
    install_requires=["voluptuous==0.11.7"],
    tests_require=["pytest"],
    entry_points={"console_scripts": ["spotifydataanalyzer=example:main"]},
)
