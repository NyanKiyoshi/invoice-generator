from setuptools import setup, find_packages
from sys import version_info


if not version_info > (3, 4):
    raise Exception('This project requires a Python version greater or equal than 3.5.')


PKG_NAME = "invoice_generator"


setup(
    author='NyanKiyoshi',
    author_email='hello@vanille.bid',
    url='https://github.com/NyanKiyoshi/invoice-generator',

    version='0.0.1.2',
    name=PKG_NAME,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    keywords=[],
    install_requires=(
        'babel',
        'weasyprint',
        'django',
    ),
    classifiers=(
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only'
    ),
)
