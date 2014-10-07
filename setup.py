# -*- coding: utf-8-*-
from setuptools import setup, find_packages

setup(
    name='lispeln',
    version='0.0.0',
    author='Leon Schröder',
    author_email='schreon.loeder@gmail.com',
    packages=find_packages(),
    url='https://github.com/schreon/lispeln',
    description='A Scheme intepreter.',
    long_description=open('README.md').read(),
    scripts=['bin/repl']
)