#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
from setuptools import setup, find_packages

CURRENT_PATH = path.abspath(path.dirname(__file__))

with open(path.join(CURRENT_PATH, 'README.md')) as readme_file:
    readme = readme_file.read()

requirements = [
    'lxml',
]

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError as e:
    requirements.append('PyQt5')

setup(
    name='pysdb',
    version='3.1.0',
    description="SDB structural database manager",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Ondrej Lexa",
    author_email='lexa.ondrej@gmail.com',
    url='https://github.com/ondrolexa/pysdb',
    license="MIT",
    python_requires=">=3.8",
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    pysdb=pysdb3.mainapp:main
    """,
    install_requires=requirements,
    zip_safe=False,
    keywords='pysdb',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities'
    ]
)
