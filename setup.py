#!/usr/bin/python

from distutils.core import setup

setup(name='kodicmd',
      description='Kodi command-line interface',
      author='Tobias D. Oestreicher',
      author_email='lists@oestreicher.com.de',
      url='https://github.com/tobias-d-oe/kodicmd',
      version='0.0.1',
      packages=['kodicmd'],
      scripts=['kodicmd/kodicmd']
)

