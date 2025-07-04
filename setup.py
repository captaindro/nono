# setup.py
from setuptools import setup, find_packages

setup(
    name="nono",
    version="0.1.0",
    packages=find_packages(),      # détecte utils/ et tests/
    include_package_data=True,
)
