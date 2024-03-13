"""setup.py module installer"""
from setuptools import setup, find_packages

with open('readme.md') as f:
    readme = f.read()

setup(
    name='zcu',
    description='ZTE Decoder Utility',
    long_description=readme,
    author='Dunia MR',
    author_email='wgalxczk3@mozmail.com',
    url='https://github.com/MichaelJorky/indihome-router-decoder',
)
