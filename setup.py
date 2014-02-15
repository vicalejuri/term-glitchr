#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

readme = open('README.md').read()

long_descrpition = """
----

%s

----
For more information, please run ``glitchr -h``
""" % ( readme )

setup(
    name="term-glitchr",
    version='0.1',
    description="Term-glitchr break and the glitchs your %terminal. Some pretty scrolling Art for the terminal.",
    author="Barrabin fc.",
    author_email="barrabin.fc@gmail.com",
    license='Unlicense - unlicense.org',
    url='https://github.com/barrabinfc/term-glitchr',
    packages=['termglitchr',],
    scripts=['bin/glitchr.py',],
    include_package_data=True,
    install_requires=['blessings>=1.5,<2.0'],
    keywords=['terminal','tty','utf8','ansii','glitch','art']
)

