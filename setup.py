"""Setup.py Module Installer"""
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()
with open('LICENSE') as f:
    LICENSE = f.read()
with open('requirements.txt') as f:
    REQUIRED = f.read()

setup(
    name='zcu',
    description='Indihome ZTE Decoder Encoder',
    long_description=readme,
    author='Dunia MR',
    author_email='wgalxczk3@mozmail.com',
    url='https://github.com/MichaelJorky/indihome-router-decoder',
    license=LICENSE,
    install_requires=REQUIRED,
    packages=find_packages(exclude=('ftp', 'telnet', 'ext', 'portscan'))
)
