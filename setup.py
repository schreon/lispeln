# -*- coding: utf-8-*-
from distutils.core import setup

setup(
    name='lispeln',
    version='0.0.0',
    author='Leon Schröder',
    author_email='schreon.loeder@gmail.com',
    packages=['lispeln'],
    url='https://github.com/schreon/lispeln',
    description='A Scheme intepreter.',
    long_description=open('README.md').read(),
    install_requires=[],
    scripts=['bin/lispeln']
)