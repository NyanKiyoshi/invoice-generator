import os.path

from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup, find_packages
from sys import version_info
import os


if not version_info > (3, 4):
    raise Exception('This project requires a Python version greater or equal than 3.5.')


HERE = os.path.dirname(__file__)
PKG_NAME = "invoice_generator"


REQUIREMENTS = [
    str(rq.req) for rq in parse_requirements(
        os.path.join(HERE, 'requirements.txt'), session=PipSession)
]


def _extract_datafiles(path, ext=None):
    if type(path) is not str:
        path = os.path.join(*path)

    extracted = []

    for root, dirs, files in os.walk(path):
        if files:
            found_files = [
                os.path.join(root, file)
                for file in files if not ext or file.endswith(ext)
            ]

            if found_files:
                extracted.append((root, found_files))

    return extracted


data_files = _extract_datafiles(('invoice_generator', 'locale'), '.mo') +\
             _extract_datafiles(('invoice_generator', 'templates'))
data_files += [
    ('', ['README.md', 'LICENSE', 'requirements.txt'])
]

print(data_files)


setup(
    version='0.0.1',
    name=PKG_NAME,
    packages=find_packages(exclude=['tests']),
    data_files=data_files,
    keywords=[],
    install_requires=REQUIREMENTS,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only'
    ],
)
