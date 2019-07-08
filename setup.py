#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c) 2017 by Mitchell Lisle
:license: MIT, see LICENSE for more details.
"""

from setuptools import setup

packages = []

setup(name='mario',
      version='OctastyNopus',
      description='A Data Engineering library',
      url='http://github.com/mitchelllisle/mario',
      author='Mitchell Lisle',
      author_email='m.lisle90@gmail.com',
      packages=['mario'],
      license='MIT',
      install_requires=packages,
      extras_require={'visualize':  ["graphviz"]},
      python_requires='>=3.6',
      zip_safe=False)
